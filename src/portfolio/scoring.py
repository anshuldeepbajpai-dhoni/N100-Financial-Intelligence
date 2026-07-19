import pandas as pd


class PortfolioScorer:

    @staticmethod
    def normalize(series):

        minimum = series.min()
        maximum = series.max()

        if maximum == minimum:
            return pd.Series([1.0] * len(series), index=series.index)

        return (series - minimum) / (maximum - minimum)

    @classmethod
    def score(cls, df):

        data = df.copy()

        data["roe_score"] = cls.normalize(data["roe_percentage"])
        data["roce_score"] = cls.normalize(data["roce_percentage"])
        data["margin_score"] = cls.normalize(data["opm_percentage"])
        data["profit_score"] = cls.normalize(data["net_profit"])
        data["marketcap_score"] = cls.normalize(data["market_cap_crore"])

        data["portfolio_score"] = (

            data["roe_score"] * 0.25 +

            data["roce_score"] * 0.25 +

            data["margin_score"] * 0.20 +

            data["profit_score"] * 0.15 +

            data["marketcap_score"] * 0.15

        )

        return data