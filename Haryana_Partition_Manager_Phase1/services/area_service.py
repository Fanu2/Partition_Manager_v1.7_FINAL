class AreaService:

    MARLAS_PER_KANAL = 20

    @staticmethod
    def kanal_marla_to_marla(
        kanal,
        marla
    ):

        return (
            float(kanal) * 20
            + float(marla)
        )

    @staticmethod
    def marla_to_kanal_marla(
        total_marla
    ):

        kanal = int(
            total_marla // 20
        )

        marla = round(
            total_marla % 20,
            2
        )

        return kanal, marla

    @staticmethod
    def format_area(
        total_marla
    ):

        kanal, marla = (
            AreaService
            .marla_to_kanal_marla(
                total_marla
            )
        )

        return (
            f"{kanal}K-{marla}M"
        )