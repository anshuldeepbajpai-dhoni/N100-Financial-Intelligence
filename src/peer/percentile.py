import pandas as pd


class PeerPercentile:
    """
    Calculates sector-wise percentile rankings
    for financial metrics.
    """

    METRICS = [
        "roe_percentage",
        "roce_percentage",
        "opm_percentage",
        "net_profit",
        "market_cap_crore"
    ]

    @classmethod
    def calculate(cls, dataframe):

        df = dataframe.copy()

        for metric in cls.METRICS:

            if metric not in df.columns:
                print(f"[INFO] {metric} not found. Skipping.")
                continue

            df[f"{metric}_percentile"] = (

                df.groupby("broad_sector")[metric]

                .rank(
                    pct=True,
                    ascending=True
                )

                * 100

            ).round(2)

        print("[INFO] Peer percentile calculation completed.")

        return df