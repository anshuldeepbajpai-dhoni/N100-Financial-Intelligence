import time

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
# ANALYTICAL QUERY ENGINE
# ==========================================================

class AnalyticalQueryEngine:

    """
    Executes analytical SQL queries against the
    N100 Financial Intelligence SQLite database.

    Features:
    - Safe read-only analytical query execution
    - Pandas DataFrame output
    - Query execution timing
    - Query result validation
    - Query execution audit generation
    - Graceful SQL error handling
    """

    def __init__(self):

        self.database = (
            DatabaseConnection()
        )

        self.query_audit = []


    # ------------------------------------------------------
    # Validate Read-Only Query
    # ------------------------------------------------------

    @staticmethod
    def is_read_only_query(
        query
    ):

        if not isinstance(
            query,
            str
        ):

            return False


        cleaned_query = (

            query
            .strip()
            .upper()

        )


        if not cleaned_query:

            return False


        # Only analytical SELECT and CTE queries
        # are permitted.

        allowed_start_keywords = (

            "SELECT",

            "WITH"

        )


        if not cleaned_query.startswith(

            allowed_start_keywords

        ):

            return False


        # Prevent database-changing SQL commands.

        blocked_keywords = [

            " INSERT ",

            " UPDATE ",

            " DELETE ",

            " DROP ",

            " ALTER ",

            " CREATE ",

            " REPLACE ",

            " TRUNCATE ",

            " ATTACH ",

            " DETACH ",

            " VACUUM ",

            " PRAGMA "

        ]


        normalized_query = (

            " "

            + " ".join(

                cleaned_query.split()

            )

            + " "

        )


        return not any(

            keyword

            in normalized_query

            for keyword

            in blocked_keywords

        )


    # ------------------------------------------------------
    # Execute One Analytical Query
    # ------------------------------------------------------

    def execute_query(

        self,

        query_name,

        query

    ):

        audit_row = {

            "query_name":
            query_name,

            "status":
            "FAILED",

            "rows_returned":
            0,

            "columns_returned":
            0,

            "execution_time_ms":
            0.0,

            "error":
            ""

        }


        start_time = (

            time.perf_counter()

        )


        try:

            # ----------------------------------------------
            # Validate Query Name
            # ----------------------------------------------

            if not query_name:

                raise ValueError(

                    "Query name cannot "
                    "be empty."

                )


            # ----------------------------------------------
            # Enforce Read-Only Query Execution
            # ----------------------------------------------

            if not (

                self.is_read_only_query(
                    query
                )

            ):

                raise ValueError(

                    "Only read-only SELECT "
                    "or WITH queries are allowed."

                )


            # ----------------------------------------------
            # Open Database Connection
            # ----------------------------------------------

            with (

                self.database
                .connect()

            ) as connection:


                # ------------------------------------------
                # Execute SQL and Return DataFrame
                # ------------------------------------------

                result = (

                    pd.read_sql_query(

                        sql=query,

                        con=connection

                    )

                )


            # ----------------------------------------------
            # Calculate Execution Time
            # ----------------------------------------------

            execution_time_ms = (

                (
                    time.perf_counter()

                    - start_time
                )

                * 1000

            )


            # ----------------------------------------------
            # Update Successful Audit
            # ----------------------------------------------

            audit_row.update(

                {

                    "status":
                    "SUCCESS",

                    "rows_returned":
                    len(
                        result
                    ),

                    "columns_returned":
                    len(
                        result.columns
                    ),

                    "execution_time_ms":
                    round(

                        execution_time_ms,

                        3

                    )

                }

            )


            logger.success(

                f"Analytical query "
                f"'{query_name}' "
                "executed successfully. "

                f"Rows: {len(result)} | "

                f"Time: "
                f"{execution_time_ms:.3f} ms"

            )


            return result


        except Exception as error:


            execution_time_ms = (

                (
                    time.perf_counter()

                    - start_time
                )

                * 1000

            )


            audit_row.update(

                {

                    "execution_time_ms":
                    round(

                        execution_time_ms,

                        3

                    ),

                    "error":
                    str(
                        error
                    )

                }

            )


            logger.error(

                f"Analytical query "
                f"'{query_name}' "
                f"failed: {error}"

            )


            return pd.DataFrame()


        finally:


            self.query_audit.append(

                audit_row

            )


    # ------------------------------------------------------
    # Export Query Execution Audit
    # ------------------------------------------------------

    def export_audit(
        self
    ):

        audit_report = (

            pd.DataFrame(
                self.query_audit
            )

        )


        output_path = (

            OUTPUT_DIR

            / "analytical_query_audit.csv"

        )


        audit_report.to_csv(

            output_path,

            index=False

        )


        logger.success(

            "Analytical query audit "
            f"saved to {output_path}"

        )


        return audit_report