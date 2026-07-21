from pathlib import Path


class ScreenerExporter:

    OUTPUT_DIR = Path("output") / "screener"

    @classmethod
    def save(cls, name, dataframe):

        cls.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_csv(
            cls.OUTPUT_DIR / f"{name}_screener.csv",
            index=False,
        )

        print(
            f"✓ Saved: {cls.OUTPUT_DIR / f'{name}_screener.csv'}"
        )

    @classmethod
    def save_all(cls, screener_results):

        cls.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        for name, dataframe in screener_results.items():

            dataframe.to_csv(
                cls.OUTPUT_DIR / f"{name}_screener.csv",
                index=False,
            )

            print(
                f"✓ Saved: {cls.OUTPUT_DIR / f'{name}_screener.csv'}"
            )