import pandas as pd


class DashboardDataset:

    @staticmethod
    def generate(portfolio_result, risk_result):

        risk = risk_result[

            [

                "company_name",

                "risk_score",

                "risk_level",

            ]

        ]

        dashboard = portfolio_result.merge(

            risk,

            on="company_name",

            how="left",

        )

        return dashboard