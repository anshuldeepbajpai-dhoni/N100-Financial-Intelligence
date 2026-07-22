import pandas as pd


class DashboardBuilder:

    def build(
        self,
        analytics_result,
        peer_result,
        sector_result,
        portfolio_result,
        risk_result
    ):

        dashboard = analytics_result[
            "results"
        ]["company_financial_snapshot"].copy()

        if "peer_comparison" in peer_result:

            peer = peer_result["peer_comparison"]

            peer_columns = [

                "company_name",

                "roe_percentage_percentile",

                "roce_percentage_percentile",

                "opm_percentage_percentile"

            ]

            available = [

                col for col in peer_columns

                if col in peer.columns

            ]

            dashboard = dashboard.merge(

                peer[available],

                on="company_name",

                how="left"

            )

        if "risk_scores" in risk_result:

            dashboard = dashboard.merge(

                risk_result["risk_scores"],

                on="company_name",

                how="left"

            )

        if "optimized_portfolio" in portfolio_result:

            dashboard = dashboard.merge(

                portfolio_result["optimized_portfolio"],

                on="company_name",

                how="left"

            )

        return dashboard