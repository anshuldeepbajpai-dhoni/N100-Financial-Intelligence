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
# DATABASE INDEX MANAGER
# ==========================================================

class DatabaseIndexManager:

    """
    Creates performance indexes for the SQLite
    financial database.

    Indexes are created only when the required
    table columns are available.
    """

    def __init__(self):

        self.database = (
            DatabaseConnection()
        )

        self.index_audit = []


    # ------------------------------------------------------
    # Get Database Tables
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

        return {

            row[1]

            for row in rows

        }


    # ------------------------------------------------------
    # Add Index Audit Result
    # ------------------------------------------------------

    def add_audit(

        self,

        table_name,

        index_name,

        indexed_columns,

        status,

        error=""

    ):

        self.index_audit.append({

            "table_name":
            table_name,

            "index_name":
            index_name,

            "indexed_columns":
            indexed_columns,

            "status":
            status,

            "error":
            error

        })


    # ------------------------------------------------------
    # Create One Index
    # ------------------------------------------------------

    def create_index(

        self,

        connection,

        table_name,

        index_name,

        columns

    ):

        column_sql = ", ".join(

            f'"{column}"'

            for column in columns

        )


        try:

            query = f"""

            CREATE INDEX IF NOT EXISTS

            "{index_name}"

            ON "{table_name}"

            ({column_sql});

            """


            connection.execute(
                query
            )


            self.add_audit(

                table_name=
                table_name,

                index_name=
                index_name,

                indexed_columns=
                ", ".join(columns),

                status=
                "SUCCESS"

            )


            logger.success(

                f"Index '{index_name}' "

                f"created for "

                f"'{table_name}'."

            )


        except Exception as error:


            self.add_audit(

                table_name=
                table_name,

                index_name=
                index_name,

                indexed_columns=
                ", ".join(columns),

                status=
                "FAILED",

                error=
                str(error)

            )


            logger.error(

                f"Index creation failed: "

                f"{index_name}: "

                f"{error}"

            )


    # ------------------------------------------------------
    # Create All Database Indexes
    # ------------------------------------------------------

    def create_all(

        self

    ):

        logger.info(

            "Starting SQLite database "

            "index creation..."

        )


        # Clear previous execution audit
        self.index_audit = []


        with (

            self.database
            .transaction()

        ) as connection:


            tables = self.get_tables(

                connection

            )


            for table_name in tables:


                columns = (

                    self.get_columns(

                        connection,

                        table_name

                    )

                )


                # ==========================================
                # COMPANY MASTER PRIMARY LOOKUP INDEX
                # ==========================================

                if (

                    table_name
                    == "companies"

                    and

                    "id"
                    in columns

                ):


                    self.create_index(

                        connection=

                        connection,

                        table_name=

                        table_name,

                        index_name=

                        "idx_companies_id",

                        columns=[

                            "id"

                        ]

                    )


                # ==========================================
                # COMPANY ID INDEX
                # ==========================================

                if (

                    "company_id"

                    in columns

                ):


                    self.create_index(

                        connection=

                        connection,

                        table_name=

                        table_name,

                        index_name=(

                            f"idx_"

                            f"{table_name}"

                            f"_company_id"

                        ),

                        columns=[

                            "company_id"

                        ]

                    )


                # ==========================================
                # FINANCIAL YEAR INDEX
                # ==========================================

                if (

                    "year"

                    in columns

                ):


                    self.create_index(

                        connection=

                        connection,

                        table_name=

                        table_name,

                        index_name=(

                            f"idx_"

                            f"{table_name}"

                            f"_year"

                        ),

                        columns=[

                            "year"

                        ]

                    )


                # ==========================================
                # COMPOSITE COMPANY-YEAR INDEX
                # ==========================================

                if {

                    "company_id",

                    "year"

                }.issubset(

                    columns

                ):


                    self.create_index(

                        connection=

                        connection,

                        table_name=

                        table_name,

                        index_name=(

                            f"idx_"

                            f"{table_name}"

                            f"_company_year"

                        ),

                        columns=[

                            "company_id",

                            "year"

                        ]

                    )


        # --------------------------------------------------
        # Generate Index Audit
        # --------------------------------------------------

        audit_report = pd.DataFrame(

            self.index_audit

        )


        output_path = (

            OUTPUT_DIR

            / "database_index_audit.csv"

        )


        audit_report.to_csv(

            output_path,

            index=False

        )


        successful_indexes = sum(

            1

            for row

            in self.index_audit

            if row["status"]

            == "SUCCESS"

        )


        failed_indexes = sum(

            1

            for row

            in self.index_audit

            if row["status"]

            == "FAILED"

        )


        logger.success(

            "Database index creation "

            "completed."

        )


        return {

            "total_indexes":

            len(
                self.index_audit
            ),

            "successful_indexes":

            successful_indexes,

            "failed_indexes":

            failed_indexes,

            "audit_report":

            audit_report

        }