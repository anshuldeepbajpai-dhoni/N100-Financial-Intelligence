# ==========================================================
# PREDEFINED FINANCIAL ANALYTICS QUERIES
# ==========================================================


class FinancialQueries:

    """
    Centralized SQL query library for the
    N100 Financial Intelligence Platform.

    All queries are read-only and execute through
    the AnalyticalQueryEngine.
    """


    # ------------------------------------------------------
    # Query 1 — Top Companies by Market Capitalization
    # ------------------------------------------------------

    TOP_COMPANIES_BY_MARKET_CAP = """

        SELECT

            company_id,

            company_name,

            year,

            market_cap_crore

        FROM company_market_performance

        WHERE market_cap_crore IS NOT NULL

        ORDER BY

            market_cap_crore DESC

        LIMIT 20

    """


    # ------------------------------------------------------
    # Query 2 — Highest ROE Companies
    # ------------------------------------------------------

    HIGHEST_ROE_COMPANIES = """

        SELECT

            company_id,

            company_name,

            roe_percentage

        FROM company_overview

        WHERE roe_percentage IS NOT NULL

        ORDER BY

            roe_percentage DESC

        LIMIT 20

    """


    # ------------------------------------------------------
    # Query 3 — Highest ROCE Companies
    # ------------------------------------------------------

    HIGHEST_ROCE_COMPANIES = """

        SELECT

            company_id,

            company_name,

            roce_percentage

        FROM company_overview

        WHERE roce_percentage IS NOT NULL

        ORDER BY

            roce_percentage DESC

        LIMIT 20

    """


    # ------------------------------------------------------
    # Query 4 — Latest Revenue and Net-Profit Ranking
    # ------------------------------------------------------

    LATEST_PROFITABILITY_RANKING = """

        WITH latest_company_year AS (

            SELECT

                company_id,

                MAX(year) AS latest_year

            FROM annual_profitability

            WHERE year IS NOT NULL

            GROUP BY

                company_id

        )

        SELECT

            profitability.company_id,

            profitability.company_name,

            profitability.year,

            profitability.sales,

            profitability.operating_profit,

            profitability.net_profit,

            profitability.opm_percentage,

            profitability.eps

        FROM annual_profitability AS profitability

        INNER JOIN latest_company_year AS latest

            ON profitability.company_id

                = latest.company_id

            AND profitability.year

                = latest.latest_year

        WHERE profitability.sales IS NOT NULL

        ORDER BY

            profitability.sales DESC

        LIMIT 25

    """


    # ------------------------------------------------------
    # Query 5 — Highest Operating-Margin Companies
    # ------------------------------------------------------

    HIGHEST_OPERATING_MARGIN = """

        WITH latest_company_year AS (

            SELECT

                company_id,

                MAX(year) AS latest_year

            FROM annual_profitability

            WHERE year IS NOT NULL

            GROUP BY

                company_id

        )

        SELECT

            profitability.company_id,

            profitability.company_name,

            profitability.year,

            profitability.sales,

            profitability.operating_profit,

            profitability.opm_percentage,

            profitability.net_profit

        FROM annual_profitability AS profitability

        INNER JOIN latest_company_year AS latest

            ON profitability.company_id

                = latest.company_id

            AND profitability.year

                = latest.latest_year

        WHERE

            profitability.opm_percentage

            IS NOT NULL

        ORDER BY

            profitability.opm_percentage DESC

        LIMIT 20

    """


    # ------------------------------------------------------
    # Query 6 — Annual Profitability Trend
    # ------------------------------------------------------

    ANNUAL_PROFITABILITY_TREND = """

        SELECT

            year,

            COUNT(
                DISTINCT company_id
            ) AS company_count,

            ROUND(
                SUM(sales),
                2
            ) AS total_sales,

            ROUND(
                SUM(operating_profit),
                2
            ) AS total_operating_profit,

            ROUND(
                SUM(net_profit),
                2
            ) AS total_net_profit,

            ROUND(
                AVG(opm_percentage),
                2
            ) AS average_operating_margin

        FROM annual_profitability

        WHERE year IS NOT NULL

        GROUP BY

            year

        ORDER BY

            year

    """


    # ------------------------------------------------------
    # Query 7 — Balance-Sheet Leverage Analysis
    # ------------------------------------------------------

    BALANCE_SHEET_LEVERAGE = """

        WITH latest_company_year AS (

            SELECT

                company_id,

                MAX(year) AS latest_year

            FROM balance_sheet_summary

            WHERE year IS NOT NULL

            GROUP BY

                company_id

        )

        SELECT

            balance.company_id,

            balance.company_name,

            balance.year,

            balance.borrowings,

            balance.total_assets,

            balance.total_liabilities,

            ROUND(

                balance.borrowings

                / NULLIF(
                    balance.total_assets,
                    0
                ),

                4

            ) AS borrowing_to_asset_ratio

        FROM balance_sheet_summary AS balance

        INNER JOIN latest_company_year AS latest

            ON balance.company_id

                = latest.company_id

            AND balance.year

                = latest.latest_year

        WHERE

            balance.borrowings

            IS NOT NULL

            AND

            balance.total_assets

            IS NOT NULL

        ORDER BY

            borrowing_to_asset_ratio DESC

        LIMIT 25

    """


    # ------------------------------------------------------
    # Query 8 — Cash-Flow Performance
    # ------------------------------------------------------

    CASHFLOW_PERFORMANCE = """

        WITH latest_company_year AS (

            SELECT

                company_id,

                MAX(year) AS latest_year

            FROM cashflow_summary

            WHERE year IS NOT NULL

            GROUP BY

                company_id

        )

        SELECT

            cashflow.company_id,

            cashflow.company_name,

            cashflow.year,

            cashflow.operating_activity,

            cashflow.investing_activity,

            cashflow.financing_activity,

            cashflow.net_cash_flow

        FROM cashflow_summary AS cashflow

        INNER JOIN latest_company_year AS latest

            ON cashflow.company_id

                = latest.company_id

            AND cashflow.year

                = latest.latest_year

        WHERE

            cashflow.operating_activity

            IS NOT NULL

        ORDER BY

            cashflow.operating_activity DESC

        LIMIT 25

    """


    # ------------------------------------------------------
    # Query 9 — Sector-Wise Company Distribution
    # ------------------------------------------------------

    SECTOR_COMPANY_DISTRIBUTION = """

        SELECT

            broad_sector,

            COUNT(
                DISTINCT company_id
            ) AS company_count

        FROM sector_company_summary

        WHERE

            broad_sector IS NOT NULL

            AND

            TRIM(
                broad_sector
            ) != ''

        GROUP BY

            broad_sector

        ORDER BY

            company_count DESC,

            broad_sector ASC

    """


    # ------------------------------------------------------
    # Query 10 — Company Financial Snapshot
    # ------------------------------------------------------

    COMPANY_FINANCIAL_SNAPSHOT = """

        WITH latest_profitability AS (

            SELECT

                company_id,

                MAX(year) AS latest_year

            FROM annual_profitability

            WHERE year IS NOT NULL

            GROUP BY

                company_id

        ),

        latest_market_cap AS (

            SELECT

                company_id,

                MAX(year) AS latest_year

            FROM company_market_performance

            WHERE year IS NOT NULL

            GROUP BY

                company_id

        )

        SELECT

            company.company_id,

            company.company_name,

            sector.broad_sector,

            company.roe_percentage,

            company.roce_percentage,

            profitability.year

                AS financial_year,

            profitability.sales,

            profitability.operating_profit,

            profitability.opm_percentage,

            profitability.net_profit,

            profitability.eps,

            market.year

                AS market_cap_year,

            market.market_cap_crore

        FROM company_overview AS company

        LEFT JOIN sector_company_summary AS sector

            ON company.company_id

                = sector.company_id

        LEFT JOIN latest_profitability

            ON company.company_id

                = latest_profitability.company_id

        LEFT JOIN annual_profitability

            AS profitability

            ON company.company_id

                = profitability.company_id

            AND profitability.year

                = latest_profitability.latest_year

        LEFT JOIN latest_market_cap

            ON company.company_id

                = latest_market_cap.company_id

        LEFT JOIN company_market_performance

            AS market

            ON company.company_id

                = market.company_id

            AND market.year

                = latest_market_cap.latest_year

        ORDER BY

            market.market_cap_crore DESC

    """


    # ------------------------------------------------------
    # Return All Queries
    # ------------------------------------------------------

    @classmethod
    def get_all_queries(
        cls
    ):

        return {

            "top_companies_by_market_cap":

            cls.TOP_COMPANIES_BY_MARKET_CAP,


            "highest_roe_companies":

            cls.HIGHEST_ROE_COMPANIES,


            "highest_roce_companies":

            cls.HIGHEST_ROCE_COMPANIES,


            "latest_profitability_ranking":

            cls.LATEST_PROFITABILITY_RANKING,


            "highest_operating_margin":

            cls.HIGHEST_OPERATING_MARGIN,


            "annual_profitability_trend":

            cls.ANNUAL_PROFITABILITY_TREND,


            "balance_sheet_leverage":

            cls.BALANCE_SHEET_LEVERAGE,


            "cashflow_performance":

            cls.CASHFLOW_PERFORMANCE,


            "sector_company_distribution":

            cls.SECTOR_COMPANY_DISTRIBUTION,


            "company_financial_snapshot":

            cls.COMPANY_FINANCIAL_SNAPSHOT

        }