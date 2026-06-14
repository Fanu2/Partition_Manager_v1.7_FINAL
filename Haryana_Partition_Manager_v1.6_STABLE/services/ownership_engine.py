from fractions import Fraction


class OwnershipEngine:

    # =====================================
    # SAFE FRACTION
    # =====================================

    @staticmethod
    def validate_fraction(
        numerator,
        denominator
    ):

        if denominator == 0:

            raise ValueError(
                "Denominator cannot be zero."
            )

        return Fraction(
            numerator,
            denominator
        )

    # =====================================
    # TOTAL SHARE
    # =====================================

    @staticmethod
    def total_share(
        ownerships
    ):

        total = Fraction(0, 1)

        for item in ownerships:

            total += Fraction(
                item.numerator,
                item.denominator
            )

        return total

    # =====================================
    # VALIDATE TOTAL SHARE
    # =====================================

    @staticmethod
    def validate_total_share(
        ownerships
    ):

        return (
            OwnershipEngine.total_share(
                ownerships
            )
            == Fraction(1, 1)
        )

    # =====================================
    # CALCULATE AREA
    # =====================================

    @staticmethod
    def calculate_area(
        total_area,
        numerator,
        denominator
    ):

        share = Fraction(
            numerator,
            denominator
        )

        return (
            float(share)
            * float(total_area)
        )

    # =====================================
    # OWNER AREA
    # =====================================

    @staticmethod
    def owner_area(
        ownership,
        total_area
    ):

        share = Fraction(
            ownership.numerator,
            ownership.denominator
        )

        return (
            float(share)
            * float(total_area)
        )

    # =====================================
    # OWNERSHIP DICTIONARY
    # =====================================

    @staticmethod
    def ownership_dict(
        ownerships
    ):

        result = {}

        for item in ownerships:

            result[item.owner_id] = Fraction(
                item.numerator,
                item.denominator
            )

        return result

    # =====================================
    # NORMALIZE SHARES
    # =====================================

    @staticmethod
    def normalize_shares(
        shares
    ):

        total = sum(
            shares.values(),
            Fraction(0, 1)
        )

        if total == 0:

            raise ValueError(
                "Total share cannot be zero."
            )

        normalized = {}

        for owner, share in shares.items():

            normalized[owner] = (
                Fraction(share)
                / total
            )

        return normalized

    # =====================================
    # SHARE TO TEXT
    # =====================================

    @staticmethod
    def fraction_text(
        fraction_value
    ):

        return (
            f"{fraction_value.numerator}/"
            f"{fraction_value.denominator}"
        )

    # =====================================
    # SHARE PERCENTAGE
    # =====================================

    @staticmethod
    def share_percentage(
        share
    ):

        return round(
            float(share) * 100,
            4
        )

    # =====================================
    # OWNERSHIP SUMMARY
    # =====================================

    @staticmethod
    def ownership_summary(
        ownerships,
        total_area
    ):

        summary = []

        for item in ownerships:

            share = Fraction(
                item.numerator,
                item.denominator
            )

            area = (
                float(share)
                * float(total_area)
            )

            summary.append(
                {
                    "owner_id":
                        item.owner_id,

                    "share":
                        str(share),

                    "area":
                        round(area, 4)
                }
            )

        return summary

    # =====================================
    # OWNERSHIP REPORT
    # =====================================

    @staticmethod
    def ownership_report(
        ownerships,
        total_area
    ):

        report = []

        for item in ownerships:

            share = Fraction(
                item.numerator,
                item.denominator
            )

            area = (
                float(share)
                * float(total_area)
            )

            report.append(
                {
                    "owner_id":
                        item.owner_id,

                    "share_fraction":
                        share,

                    "share_text":
                        (
                            f"{share.numerator}/"
                            f"{share.denominator}"
                        ),

                    "percentage":
                        round(
                            float(share) * 100,
                            4
                        ),

                    "area":
                        round(area, 4)
                }
            )

        return report

    # =====================================
    # REMAINING SHARE
    # =====================================

    @staticmethod
    def remaining_share(
        original_share,
        removed_share
    ):

        return (
            Fraction(original_share)
            - Fraction(removed_share)
        )

    # =====================================
    # IS FULL OWNER
    # =====================================

    @staticmethod
    def is_full_owner(
        ownership
    ):

        share = Fraction(
            ownership.numerator,
            ownership.denominator
        )

        return share == Fraction(1, 1)

    # =====================================
    # SHARE FROM AREA
    # =====================================

    @staticmethod
    def area_to_share(
        area,
        total_area
    ):

        if total_area <= 0:

            raise ValueError(
                "Total area must be positive."
            )

        return Fraction(
            area / total_area
        ).limit_denominator()