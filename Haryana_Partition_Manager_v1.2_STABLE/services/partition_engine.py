from fractions import Fraction

from database.db import SessionLocal

from database.models import (
    Khewat,
    Ownership,
    Khasra
)

from services.khewat_service import (
    KhewatService
)

from services.ownership_engine import (
    OwnershipEngine
)


class PartitionEngine:

    @staticmethod
    def partition(
        source_khewat_id,
        selected_owner_ids,
        selected_khasra_ids,
        new_khewat_no,
        new_khatauni_no="",
        remarks=""
    ):

        session = SessionLocal()

        try:

            source = session.get(
                Khewat,
                source_khewat_id
            )

            if not source:
                raise ValueError("Source Khewat not found.")

            ownerships = (
                session.query(Ownership)
                .filter(
                    Ownership.khewat_id == source_khewat_id
                )
                .all()
            )

            selected_ownerships = []
            remaining_ownerships = []

            for item in ownerships:

                if item.owner_id in selected_owner_ids:
                    selected_ownerships.append(item)
                else:
                    remaining_ownerships.append(item)

            if not selected_ownerships:
                raise ValueError("No owners selected.")

            khasras = (
                session.query(Khasra)
                .filter(
                    Khasra.khewat_id == source_khewat_id
                )
                .all()
            )

            selected_khasras = []

            for khasra in khasras:

                if khasra.id in selected_khasra_ids:
                    selected_khasras.append(khasra)

            if not selected_khasras:
                raise ValueError("No khasras selected.")

            selected_area = sum(
                k.area for k in selected_khasras
            )

            remaining_area = (
                source.total_area - selected_area
            )

            selected_shares = {}

            for item in selected_ownerships:

                selected_shares[item.owner_id] = Fraction(
                    item.numerator,
                    item.denominator
                )

            selected_shares = OwnershipEngine.normalize_shares(
                selected_shares
            )

            ownership_data = []

            for owner_id, share in selected_shares.items():

                ownership_data.append(
                    {
                        "owner_id": owner_id,
                        "numerator": share.numerator,
                        "denominator": share.denominator
                    }
                )

            khasra_data = []

            for khasra in selected_khasras:

                khasra_data.append(
                    {
                        "khasra_no": khasra.khasra_no,
                        "area": khasra.area
                    }
                )

            new_khewat = KhewatService.create_khewat(
                village_id=source.village_id,
                khewat_no=new_khewat_no,
                khatauni_no=new_khatauni_no,
                total_area=selected_area,
                ownerships=ownership_data,
                khasras=khasra_data,
                status="PARTITIONED",
                remarks=remarks
            )

            for khasra in selected_khasras:
                session.delete(khasra)

            remaining_shares = {}

            for item in remaining_ownerships:

                remaining_shares[item.owner_id] = Fraction(
                    item.numerator,
                    item.denominator
                )

            if remaining_shares:

                remaining_shares = OwnershipEngine.normalize_shares(
                    remaining_shares
                )

                for item in remaining_ownerships:

                    share = remaining_shares[item.owner_id]

                    item.numerator = share.numerator
                    item.denominator = share.denominator

            
            source.total_area = remaining_area

            session.commit()

            # Save values before object becomes detached

            new_khewat_id = new_khewat["id"]
            new_khewat_no_value = new_khewat["khewat_no"]

            KhewatService.create_partition_event(
                source_khewat_id=source.id,
                new_khewat_id=new_khewat_id,
                removed_area=selected_area,
                owners_removed=selected_owner_ids,
                remarks=remarks
            )

            return {
                "id": new_khewat_id,
                "khewat_no": new_khewat_no_value
            }

        except Exception:

            session.rollback()
            raise

        finally:

            session.close()


