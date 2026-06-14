from fractions import Fraction

from database.db import SessionLocal

from database.models import (
    Khewat,
    Ownership,
    Khasra,
    PartitionEvent
)

from services.ownership_engine import (
    OwnershipEngine
)


class KhewatService:

    # =====================================
    # CREATE KHEWAT
    # =====================================

    @staticmethod
    def create_khewat(
        village_id,
        khewat_no,
        khatauni_no,
        total_area,
        ownerships,
        khasras,
        status="JOINT",
        remarks=""
    ):

        session = SessionLocal()

        try:

            existing = (
                session.query(Khewat)
                .filter(
                    Khewat.village_id == village_id,
                    Khewat.khewat_no == khewat_no
                )
                .first()
            )

            if existing:

                raise ValueError(
                    "Khewat already exists."
                )

            total_share = Fraction(0, 1)

            for item in ownerships:

                total_share += Fraction(
                    item["numerator"],
                    item["denominator"]
                )

            if total_share != Fraction(1, 1):

                raise ValueError(
                    "Ownership share must equal 1."
                )

            khasra_total = sum(
                x["area"]
                for x in khasras
            )

            if abs(
                khasra_total - total_area
            ) > 0.01:

                raise ValueError(
                    "Khasra area mismatch."
                )

            khewat = Khewat(

                village_id=village_id,

                khewat_no=khewat_no,

                khatauni_no=khatauni_no,

                total_area=total_area,

                status=status,

                remarks=remarks
            )

            session.add(
                khewat
            )

            session.flush()

            for item in ownerships:

                session.add(

                    Ownership(

                        khewat_id=khewat.id,

                        owner_id=item[
                            "owner_id"
                        ],

                        numerator=item[
                            "numerator"
                        ],

                        denominator=item[
                            "denominator"
                        ]
                    )
                )

            for item in khasras:

                session.add(

                    Khasra(

                        khewat_id=khewat.id,

                        khasra_no=item[
                            "khasra_no"
                        ],

                        area=item[
                            "area"
                        ]
                    )
                )

            session.commit()

            return khewat

        except:

            session.rollback()

            raise

        finally:

            session.close()

    # =====================================
    # DELETE KHEWAT
    # =====================================

    @staticmethod
    def delete_khewat(
        khewat_id
    ):

        session = SessionLocal()

        try:

            khewat = session.get(
                Khewat,
                khewat_id
            )

            if not khewat:

                raise ValueError(
                    "Khewat not found."
                )

            session.delete(
                khewat
            )

            session.commit()

        except:

            session.rollback()

            raise

        finally:

            session.close()

    # =====================================
    # GET SHARES
    # =====================================

    @staticmethod
    def get_share_dict(
        khewat_id
    ):

        session = SessionLocal()

        try:

            ownerships = (
                session.query(
                    Ownership
                )
                .filter(
                    Ownership.khewat_id
                    == khewat_id
                )
                .all()
            )

            return (
                OwnershipEngine
                .ownership_dict(
                    ownerships
                )
            )

        finally:

            session.close()

    # =====================================
    # CREATE PARTITION EVENT
    # =====================================

    @staticmethod
    def create_partition_event(
        source_khewat_id,
        new_khewat_id,
        removed_area,
        owners_removed,
        remarks=""
    ):

        session = SessionLocal()

        try:

            event = PartitionEvent(

                source_khewat_id=
                source_khewat_id,

                new_khewat_id=
                new_khewat_id,

                removed_area=
                removed_area,

                owners_removed=
                ",".join(
                    map(
                        str,
                        owners_removed
                    )
                ),

                remarks=remarks
            )

            session.add(
                event
            )

            session.commit()

            return event

        except:

            session.rollback()

            raise

        finally:

            session.close()