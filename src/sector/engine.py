import pandas as pd


class SectorEngine:

    def analyze(self, snapshot):

        sector_summary = (

            snapshot

            .groupby("broad_sector")

            .agg(

                companies=("company_name", "count"),

                avg_roe=("roe_percentage", "mean"),

                avg_roce=("roce_percentage", "mean"),

                avg_opm=("opm_percentage", "mean"),

                avg_net_profit=("net_profit", "mean"),

                total_market_cap=("market_cap_crore", "sum")

            )

            .reset_index()

        )

        sector_rankings = (

            sector_summary

            .sort_values(

                by="avg_roe",

                ascending=False

            )

            .reset_index(drop=True)

        )

        return {

            "sector_summary": sector_summary,

            "sector_rankings": sector_rankings

        }