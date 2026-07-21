import yaml

from pathlib import Path

from .filters import (
    min_filter,
    max_filter,
    debt_equity_filter,
    interest_coverage_filter,
)
from .presets import PRESET_SCREENERS


class ScreenerEngine:

    def __init__(self):

        config = (
            Path(__file__).resolve().parent.parent
            / "config"
            / "screener_config.yaml"
        )

        with open(config) as file:

            self.config = yaml.safe_load(file)

    def run(
        self,
        ratios_df,
        thresholds,
    ):

        df = ratios_df.copy()

        # Rename columns from analytics output
        df = df.rename(columns={
            "roe_percentage": "roe",
            "roce_percentage": "roce",
            "opm_percentage": "opm",
            "market_cap_crore": "market_cap"
        })

        metrics = self.config["metrics"]

        for metric, threshold in thresholds.items():

            if threshold is None:
                continue

            if metric not in metrics:
                print(f"[INFO] Metric '{metric}' not configured. Skipping.")
                continue

            rule = metrics[metric]

            column = rule["column"]

            # Skip filters whose columns don't exist
            if column not in df.columns:
                continue

            operator = rule["operator"]

            if metric == "debt_equity":

                df = debt_equity_filter(
                    df,
                    column,
                    threshold,
                )

            elif metric == "interest_coverage":

                df = interest_coverage_filter(
                    df,
                    column,
                    threshold,
                )

            elif operator == "min":

                df = min_filter(
                    df,
                    column,
                    threshold,
                )

            elif operator == "max":

                df = max_filter(
                    df,
                    column,
                    threshold,
                )


        # ---------------------------------------------------------
        # Composite Quality Score
        # ---------------------------------------------------------

        df["composite_quality_score"] = 0.0

        if "roe" in df.columns:
            df["composite_quality_score"] += df["roe"] * 0.30

        if "roce" in df.columns:
            df["composite_quality_score"] += df["roce"] * 0.25

        if "opm" in df.columns:
            df["composite_quality_score"] += df["opm"] * 0.15

        if "net_profit" in df.columns:
            df["composite_quality_score"] += (
                df["net_profit"] / df["net_profit"].max()
            ) * 15

        if "market_cap" in df.columns:
            df["composite_quality_score"] += (
                df["market_cap"] / df["market_cap"].max()
            ) * 15

        return (
            df.sort_values(
                "composite_quality_score",
                ascending=False
            )
            .reset_index(drop=True)
        )  
    
    from .presets import PRESET_SCREENERS


    def run_preset(
        self,
        ratios_df,
        preset_name,
    ):

        thresholds = PRESET_SCREENERS[preset_name]

        return self.run(
            ratios_df,
            thresholds,
        )