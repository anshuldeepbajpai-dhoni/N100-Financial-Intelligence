from pathlib import Path


class DashboardExporter:

    OUTPUT = Path("output") / "dashboard"

    @classmethod
    def save(cls, dataframe):

        cls.OUTPUT.mkdir(

            parents=True,

            exist_ok=True

        )

        dataframe.to_csv(

            cls.OUTPUT / "dashboard_dataset.csv",

            index=False

        )

        print("\nDashboard Dataset Exported Successfully.\n")