import pandas as pd

from src.database.connection import (
    DatabaseConnection
)

from src.etl.config import (
    OUTPUT_DIR
)

from src.etl.logger import (
    logger
)


# ==========================================================
# ANALYTICAL SQL VIEW MANAGER
# ==========================================================

class AnalyticalViewManager:

    """
    Creates and validates reusable analytical SQL
    views for the N100 Financial Intelligence Platform.
    """

    def __init__(self):

        self.database = (
            DatabaseConnection()
        )

        self.view_audit = []


    # ------------------------------------------------------
    # Analytical View Definitions
    # ------------------------------------------------------

    @staticmethod
    def get_view_definitions():

        return {

            # ==================================================
            # VIEW 1 — COMPANY OVERVIEW
            # ==================================================

            "company_overview": """

                SELECT

                    id AS company_id,

                    company_name,

                    website,

                    face_value,

                    book_value,

                    roce_percentage,

                    roe_percentage

                FROM companies

            """,


            # ==================================================
            # VIEW 2 — ANNUAL PROFITABILITY
            # ==================================================

            "annual_profitability": """

                SELECT

                    p.company_id,

                    c.company_name,

                    p.year,

                    p.sales,

                    p.operating_profit,

                    p.opm_percentage,

                    p.net_profit,

                    p.tax_percentage,

                    p.eps,

                    p.dividend_payout

                FROM profitandloss p

                LEFT JOIN companies c

                    ON p.company_id = c.id

            """,


            # ==================================================
            # VIEW 3 — BALANCE-SHEET SUMMARY
            # ==================================================

            "balance_sheet_summary": """

                SELECT

                    b.company_id,

                    c.company_name,

                    b.year,

                    b.equity_capital,

                    b.reserves,

                    b.borrowings,

                    b.other_liabilities,

                    b.total_liabilities,

                    b.fixed_assets,

                    b.cwip,

                    b.investments,

                    b.other_asset,

                    b.total_assets

                FROM balancesheet b

                LEFT JOIN companies c

                    ON b.company_id = c.id

            """,


            # ==================================================
            # VIEW 4 — CASH-FLOW SUMMARY
            # ==================================================

            "cashflow_summary": """

                SELECT

                    cf.company_id,

                    c.company_name,

                    cf.year,

                    cf.operating_activity,

                    cf.investing_activity,

                    cf.financing_activity,

                    cf.net_cash_flow

                FROM cashflow cf

                LEFT JOIN companies c

                    ON cf.company_id = c.id

            """,


            # ==================================================
            # VIEW 5 — FINANCIAL-RATIO SUMMARY
            # ==================================================

            "financial_ratio_summary": """

                SELECT

                    fr.company_id,

                    c.company_name,

                    fr.year,

                    fr.net_profit_margin_pct,

                    fr.operating_profit_margin_pct,

                    fr.interest_coverage,

                    fr.asset_turnover,

                    fr.free_cash_flow_cr,

                    fr.capex_cr,

                    fr.earnings_per_share,

                    fr.dividend_payout_ratio_pct,

                    fr.cash_from_operations_cr

                FROM financial_ratios fr

                LEFT JOIN companies c

                    ON fr.company_id = c.id

            """,


            # ==================================================
            # VIEW 6 — COMPANY MARKET PERFORMANCE
            # ==================================================

            "company_market_performance": """

                SELECT

                    mc.company_id,

                    c.company_name,

                    mc.year,

                    mc.market_cap_crore

                FROM market_cap mc

                LEFT JOIN companies c

                    ON mc.company_id = c.id

            """,

            # ==================================================
            # VIEW 7 — SECTOR COMPANY SUMMARY
            # ==================================================

            "sector_company_summary": """

                SELECT

                    s.company_id,

                    c.company_name,

                    s.broad_sector

                FROM sectors s

                LEFT JOIN companies c

                    ON s.company_id = c.id

            """

        }


    # ------------------------------------------------------
    # Create One Analytical View
    # ------------------------------------------------------

    def create_view(

        self,

        connection,

        view_name,

        select_query

    ):

        audit_row = {

            "view_name":
            view_name,

            "status":
            "FAILED",

            "row_count":
            0,

            "column_count":
            0,

            "error":
            ""

        }


        try:

            # ----------------------------------------------
            # Remove Existing View
            # ----------------------------------------------

            connection.execute(

                f"""
                DROP VIEW IF EXISTS
                "{view_name}";
                """

            )


            # ----------------------------------------------
            # Create New View
            # ----------------------------------------------

            connection.execute(

                f"""
                CREATE VIEW
                "{view_name}"

                AS

                {select_query};
                """

            )


            # ----------------------------------------------
            # Validate View Row Count
            # ----------------------------------------------

            result = connection.execute(

                f"""
                SELECT COUNT(*)
                FROM "{view_name}";
                """

            ).fetchone()


            row_count = int(

                result[0]

            )


            # ----------------------------------------------
            # Validate View Columns
            # ----------------------------------------------

            columns = connection.execute(

                f"""
                PRAGMA table_info(
                    "{view_name}"
                );
                """

            ).fetchall()


            audit_row[
                "row_count"
            ] = row_count


            audit_row[
                "column_count"
            ] = len(
                columns
            )


            audit_row[
                "status"
            ] = "SUCCESS"


            logger.success(

                f"Analytical view "
                f"'{view_name}' "
                "created successfully."

            )


        except Exception as error:


            audit_row[
                "error"
            ] = str(
                error
            )


            logger.error(

                f"Analytical view "
                f"'{view_name}' "
                f"failed: {error}"

            )


        self.view_audit.append(

            audit_row

        )


        return (

            audit_row["status"]

            == "SUCCESS"

        )


    # ------------------------------------------------------
    # Create All Analytical Views
    # ------------------------------------------------------

    def create_all(

        self

    ):

        logger.info(

            "Starting analytical SQL "
            "view creation..."

        )


        # Clear audit from previous execution
        self.view_audit = []


        view_definitions = (

            self.get_view_definitions()

        )


        with (

            self.database
            .transaction()

        ) as connection:


            for (

                view_name,

                select_query

            ) in (

                view_definitions.items()

            ):


                self.create_view(

                    connection=

                    connection,

                    view_name=

                    view_name,

                    select_query=

                    select_query

                )


        # --------------------------------------------------
        # Generate SQL View Validation Report
        # --------------------------------------------------

        audit_report = pd.DataFrame(

            self.view_audit

        )


        output_path = (

            OUTPUT_DIR

            / "sql_view_validation.csv"

        )


        audit_report.to_csv(

            output_path,

            index=False

        )


        successful_views = sum(

            1

            for row

            in self.view_audit

            if row["status"]

            == "SUCCESS"

        )


        failed_views = sum(

            1

            for row

            in self.view_audit

            if row["status"]

            == "FAILED"

        )


        logger.success(

            "Analytical SQL view "
            "creation completed."

        )


        return {

            "total_views":

            len(
                self.view_audit
            ),

            "successful_views":

            successful_views,

            "failed_views":

            failed_views,

            "audit_report":

            audit_report

        }