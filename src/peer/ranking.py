import pandas as pd


class PeerRanking:

    @staticmethod
    def rank(df):

        df = df.copy()

        metrics = [
            "roe_percentage",
            "roce_percentage",
            "opm_percentage",
            "net_profit",
            "market_cap_crore",
        ]

        for metric in metrics:

            if metric in df.columns:

                df[f"{metric}_rank"] = (
                    df.groupby("broad_sector")[metric]
                    .rank(
                        ascending=False,
                        method="dense",
                    )
                )

        return df