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
# DATABASE INTEGRITY CHECKER
# ==========================================================

class DatabaseIntegrityChecker:

    """
    Performs structural and data-integrity checks
    on the N100 SQLite database.
    """

    def __init__(self):

        self.database = (
            DatabaseConnection()
        )

        self.results = []

        self.table_summary = []


    # ------------------------------------------------------
    # Add Integrity Result
    # ------------------------------------------------------

    def add_result(
        self,
        table_name,
        check_name,
        severity,
        failures,
        details=""
    ):

        self.results.append({

            "table_name": table_name,

            "check": check_name,

            "severity": severity,

            "failures": int(
                failures
            ),

            "details": details

        })


    # ------------------------------------------------------
    # Get All User Tables
    # ------------------------------------------------------

    @staticmethod
    def get_tables(
        connection
    ):

        query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
        """

        rows = connection.execute(
            query
        ).fetchall()

        return [

            row[0]

            for row in rows

        ]


    # ------------------------------------------------------
    # Get Table Columns
    # ------------------------------------------------------

    @staticmethod
    def get_columns(
        connection,
        table_name
    ):

        rows = connection.execute(

            f"""
            PRAGMA table_info(
                "{table_name}"
            );
            """

        ).fetchall()

        return [

            row[1]

            for row in rows

        ]


    # ------------------------------------------------------
    # Get Table Row Count
    # ------------------------------------------------------

    @staticmethod
    def get_row_count(
        connection,
        table_name
    ):

        result = connection.execute(

            f"""
            SELECT COUNT(*)
            FROM "{table_name}";
            """

        ).fetchone()

        return int(
            result[0]
        )


    # ------------------------------------------------------
    # Check Expected Tables
    # ------------------------------------------------------

    def check_expected_tables(
        self,
        actual_tables
    ):

        expected_tables = {

            "companies",

            "profitandloss",

            "balancesheet",

            "cashflow",

            "analysis",

            "documents",

            "prosandcons",

            "sectors",

            "stock_prices",

            "market_cap",

            "financial_ratios",

            "peer_groups"

        }


        missing_tables = (

            expected_tables

            - set(actual_tables)

        )


        self.add_result(

            table_name="DATABASE",

            check_name=(
                "EXPECTED_TABLES"
            ),

            severity="CRITICAL",

            failures=len(
                missing_tables
            ),

            details=(

                ", ".join(

                    sorted(
                        missing_tables
                    )

                )

                if missing_tables

                else

                "All expected tables exist."

            )

        )


    # ------------------------------------------------------
    # Check Empty Tables
    # ------------------------------------------------------

    def check_empty_table(
        self,
        table_name,
        row_count
    ):

        failures = (

            1

            if row_count == 0

            else 0

        )


        self.add_result(

            table_name=table_name,

            check_name="EMPTY_TABLE",

            severity="CRITICAL",

            failures=failures,

            details=(

                "Table contains no records."

                if failures

                else

                f"{row_count} records found."

            )

        )


    # ------------------------------------------------------
    # Check Missing Company IDs
    # ------------------------------------------------------

    def check_missing_company_id(
        self,
        connection,
        table_name,
        columns
    ):

        if "company_id" not in columns:

            return


        result = connection.execute(

            f"""
            SELECT COUNT(*)
            FROM "{table_name}"
            WHERE company_id IS NULL
            OR TRIM(
                CAST(
                    company_id AS TEXT
                )
            ) = '';
            """

        ).fetchone()


        failures = int(
            result[0]
        )


        self.add_result(

            table_name=table_name,

            check_name=(
                "MISSING_COMPANY_ID"
            ),

            severity="CRITICAL",

            failures=failures,

            details=(

                f"{failures} missing "
                "company identifiers."

            )

        )


    # ------------------------------------------------------
    # Check Invalid Financial Years
    # ------------------------------------------------------

    def check_invalid_year(
        self,
        connection,
        table_name,
        columns
    ):

        if "year" not in columns:

            return


        result = connection.execute(

            f"""
            SELECT COUNT(*)
            FROM "{table_name}"
            WHERE year IS NULL
            OR CAST(
                year AS INTEGER
            ) < 1900
            OR CAST(
                year AS INTEGER
            ) > 2100;
            """

        ).fetchone()


        failures = int(
            result[0]
        )


        self.add_result(

            table_name=table_name,

            check_name="INVALID_YEAR",

            severity="CRITICAL",

            failures=failures,

            details=(

                f"{failures} invalid or "
                "missing financial years."

            )

        )


    # ------------------------------------------------------
    # Check Orphan Company References
    # ------------------------------------------------------

    def check_orphan_company_ids(
        self,
        connection,
        table_name,
        columns
    ):

        if (

            table_name == "companies"

            or

            "company_id"
            not in columns

        ):

            return


        result = connection.execute(

            f"""
            SELECT COUNT(*)

            FROM "{table_name}" child

            LEFT JOIN companies parent

            ON child.company_id
            = parent.id

            WHERE child.company_id
            IS NOT NULL

            AND parent.id IS NULL;
            """

        ).fetchone()


        failures = int(
            result[0]
        )


        self.add_result(

            table_name=table_name,

            check_name=(
                "ORPHAN_COMPANY_REFERENCE"
            ),

            severity="CRITICAL",

            failures=failures,

            details=(

                f"{failures} records reference "
                "companies missing from the "
                "company master."

            )

        )


    # ------------------------------------------------------
    # Check Duplicate Company-Year Keys
    # ------------------------------------------------------

    def check_duplicate_company_year(
        self,
        connection,
        table_name,
        columns
    ):

        required_columns = {

            "company_id",

            "year"

        }


        if not required_columns.issubset(

            set(columns)

        ):

            return


        result = connection.execute(

            f"""
            SELECT
                COALESCE(
                    SUM(record_count),
                    0
                )

            FROM
            (
                SELECT

                    COUNT(*) AS
                    record_count

                FROM "{table_name}"

                WHERE company_id
                IS NOT NULL

                AND year
                IS NOT NULL

                GROUP BY

                    company_id,

                    year

                HAVING COUNT(*) > 1
            );
            """

        ).fetchone()


        failures = int(

            result[0] or 0

        )


        self.add_result(

            table_name=table_name,

            check_name=(

                "DUPLICATE_"
                "COMPANY_YEAR"

            ),

            severity="WARNING",

            failures=failures,

            details=(

                f"{failures} records belong "
                "to duplicate company-year "
                "groups."

            )

        )


    # ------------------------------------------------------
    # Validate Complete Database
    # ------------------------------------------------------

    def validate_all(
        self
    ):

        logger.info(

            "Starting SQLite database "
            "integrity validation..."

        )


        # Clear previous execution results
        self.results = []

        self.table_summary = []


        with (

            self.database
            .transaction()

        ) as connection:


            tables = self.get_tables(
                connection
            )


            self.check_expected_tables(
                tables
            )


            for table_name in tables:


                columns = self.get_columns(

                    connection,

                    table_name

                )


                row_count = (

                    self.get_row_count(

                        connection,

                        table_name

                    )

                )


                self.table_summary.append({

                    "table_name":
                    table_name,

                    "rows":
                    row_count,

                    "columns":
                    len(columns),

                    "status":

                    "EMPTY"

                    if row_count == 0

                    else

                    "AVAILABLE"

                })


                self.check_empty_table(

                    table_name,

                    row_count

                )


                self.check_missing_company_id(

                    connection,

                    table_name,

                    columns

                )


                self.check_invalid_year(

                    connection,

                    table_name,

                    columns

                )


                self.check_orphan_company_ids(

                    connection,

                    table_name,

                    columns

                )


                self.check_duplicate_company_year(

                    connection,

                    table_name,

                    columns

                )


        integrity_report = pd.DataFrame(

            self.results

        )


        table_report = pd.DataFrame(

            self.table_summary

        )


        integrity_path = (

            OUTPUT_DIR

            / "database_integrity_report.csv"

        )


        table_path = (

            OUTPUT_DIR

            / "database_table_summary.csv"

        )


        integrity_report.to_csv(

            integrity_path,

            index=False

        )


        table_report.to_csv(

            table_path,

            index=False

        )


        logger.success(

            "Database integrity reports "
            "generated successfully."

        )


        return (

            integrity_report,

            table_report

        )