import pandas as pd

from pathlib import Path

from .forecast_engine import ForecastEngine
from .export import ForecastExporter


class ForecastRunner:

    def __init__(self):

        self.engine = ForecastEngine()

    def run(self, datasets):

        profit = datasets["profitandloss.xlsx"]
        cashflow = datasets["cashflow.xlsx"]

        profit_metrics = [
            "sales",
            "operating_profit",
            "net_profit",
            "eps",
        ]

        cashflow_metrics = [
            "net_cash_flow",
        ]

        profit_forecasts = self.engine.forecast_multiple(
            profit,
            profit_metrics,
        )

        cashflow_forecasts = self.engine.forecast_multiple(
            cashflow,
            cashflow_metrics,
        )

        ForecastExporter.save_all(profit_forecasts)
        ForecastExporter.save_all(cashflow_forecasts)

        # ---------------------------------------
        # Forecast Summary
        # ---------------------------------------

        summary_rows = []

        all_forecasts = {
            **profit_forecasts,
            **cashflow_forecasts,
        }

        for metric, df in all_forecasts.items():

            summary_rows.append({

                "metric": metric,

                "latest_value": df.iloc[-1]["forecast"],

                "forecast_points": len(df)

            })

        summary = pd.DataFrame(summary_rows)

        output = Path("output") / "forecasting"
        output.mkdir(parents=True, exist_ok=True)

        summary.to_csv(
            output / "forecast_summary.csv",
            index=False
        )

        summary.to_csv(
            output / "forecast_metrics.csv",
            index=False
        )

        print("\nForecasting completed.\n")

        return all_forecasts