import pandas as pd


class ExecutiveSummary:

    @staticmethod
    def generate(analytics_result, portfolio_result, risk_result):

        summary = {

            "Total Companies Analyzed":
                len(
                    analytics_result["results"]["company_financial_snapshot"]
                ),

            "Portfolio Companies":
                len(portfolio_result),

            "Low Risk Companies":
                (risk_result["risk_level"] == "Low").sum(),

            "Medium Risk Companies":
                (risk_result["risk_level"] == "Medium").sum(),

            "High Risk Companies":
                (risk_result["risk_level"] == "High").sum(),

            "Average Portfolio Score":
                round(
                    portfolio_result["portfolio_score"].mean(),
                    2,
                ),

            "Average Risk Score":
                round(
                    risk_result["risk_score"].mean(),
                    2,
                ),

            "Best Company":

                portfolio_result.iloc[0]["company_name"],

            "Top Sector":

                portfolio_result["broad_sector"]

                .mode()

                .iloc[0],

        }

        return pd.DataFrame([summary])