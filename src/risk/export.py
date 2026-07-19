from pathlib import Path


class RiskExporter:

    OUTPUT = Path("output/risk")

    @classmethod
    def save(cls, scores, summary):

        cls.OUTPUT.mkdir(

            parents=True,

            exist_ok=True,

        )

        scores.to_csv(

            cls.OUTPUT / "risk_scores.csv",

            index=False,

        )

        summary.to_csv(

            cls.OUTPUT / "risk_summary.csv",

            index=False,

        )

        print("Risk reports exported successfully.")