from pathlib import Path


class SectorExporter:

    OUTPUT = Path("output") / "sector"

    @classmethod
    def save_all(cls, results):

        cls.OUTPUT.mkdir(
            parents=True,
            exist_ok=True,
        )

        results["sector_summary"].to_csv(
            cls.OUTPUT / "sector_summary.csv",
            index=False,
        )

        results["sector_rankings"].to_csv(
            cls.OUTPUT / "sector_rankings.csv",
            index=False,
        )

        print("\nSector Analytics Exported Successfully.")