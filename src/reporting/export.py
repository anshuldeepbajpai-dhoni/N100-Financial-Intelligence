from pathlib import Path


class ReportExporter:

    OUTPUT = Path("output/reporting")

    @classmethod
    def save(

        cls,

        summary,

        dashboard,

    ):

        cls.OUTPUT.mkdir(

            parents=True,

            exist_ok=True,

        )

        summary.to_csv(

            cls.OUTPUT /

            "executive_summary.csv",

            index=False,

        )

        dashboard.to_csv(

            cls.OUTPUT /

            "dashboard_dataset.csv",

            index=False,

        )

        print(

            "Executive reports exported successfully."

        )