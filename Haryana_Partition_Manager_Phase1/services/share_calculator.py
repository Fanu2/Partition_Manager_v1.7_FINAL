from fractions import Fraction

from services.area_service import (
    AreaService
)


class ShareCalculator:

    @staticmethod
    def share_area(
        total_marla,
        numerator,
        denominator
    ):

        share = Fraction(
            numerator,
            denominator
        )

        area = float(
            share * total_marla
        )

        return area

    @staticmethod
    def share_text(
        total_marla,
        numerator,
        denominator
    ):

        area = (
            ShareCalculator.share_area(
                total_marla,
                numerator,
                denominator
            )
        )

        return (
            AreaService
            .format_area(area)
        )