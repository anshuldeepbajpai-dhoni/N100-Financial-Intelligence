import pandas as pd


class RiskSummary:

    @staticmethod
    def generate(df):

        summary = {

            "Total Companies": len(df),

            "Low Risk": (df["risk_level"] == "Low").sum(),

            "Medium Risk": (df["risk_level"] == "Medium").sum(),

            "High Risk": (df["risk_level"] == "High").sum(),

            "Average Risk Score": round(

                df["risk_score"].mean(),

                2,

            ),

            "Average ROE": round(

                df["roe_percentage"].mean(),

                2,

            ),

            "Average ROCE": round(

                df["roce_percentage"].mean(),

                2,

            ),

            "Average OPM": round(

                df["opm_percentage"].mean(),

                2,

            ),

        }

        return pd.DataFrame([summary])