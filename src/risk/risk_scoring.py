import pandas as pd


class RiskScorer:

    @staticmethod
    def normalize(series):

        minimum = series.min()
        maximum = series.max()

        if maximum == minimum:
            return pd.Series(
                [0.5] * len(series),
                index=series.index
            )

        return (series - minimum) / (maximum - minimum)

    @classmethod
    def calculate(cls, portfolio):

        df = portfolio.copy()

        df["roe_risk"] = 1 - cls.normalize(df["roe_percentage"])
        df["roce_risk"] = 1 - cls.normalize(df["roce_percentage"])
        df["margin_risk"] = 1 - cls.normalize(df["opm_percentage"])

        df["risk_score"] = (

            df["roe_risk"] * 0.40 +

            df["roce_risk"] * 0.30 +

            df["margin_risk"] * 0.30

        ) * 100

        def classify(score):

            if score < 30:
                return "Low"

            elif score < 60:
                return "Medium"

            return "High"

        df["risk_level"] = df["risk_score"].apply(classify)

        return df