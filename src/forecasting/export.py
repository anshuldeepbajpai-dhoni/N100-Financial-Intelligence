from pathlib import Path

import pandas as pd


class ForecastExporter:

    OUTPUT = Path("output")

    @classmethod
    def save(cls, df, filename):

        cls.OUTPUT.mkdir(exist_ok=True)

        df.to_csv(
            cls.OUTPUT / filename,
            index=False,
        )

    @classmethod
    def save_all(cls, forecasts):

        for metric, df in forecasts.items():

            filename = f"{metric}_forecast.csv"

            cls.save(df, filename)

        print("\nForecast files exported successfully.\n")