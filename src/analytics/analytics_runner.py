from pathlib import Path

import pandas as pd

from src.analytics.query_engine import (
    AnalyticalQueryEngine
)

from src.analytics.financial_queries import (
    FinancialQueries
)

from src.etl.config import (
    OUTPUT_DIR
)

from src.etl.logger import (
    logger
)


# ==========================================================
# FINANCIAL ANALYTICS RUNNER
# ==========================================================

class FinancialAnalyticsRunner:

    """
    Executes all predefined financial analytics queries
    and exports their results as CSV files.

    Features:
    - Executes every predefined financial query
    - Exports successful query results
    - Records output row and column counts
    - Generates an analytics export manifest
    - Generates a query-execution audit
    - Continues execution if an individual query fails
    """

    def __init__(self):

        # --------------------------------------------------
        # Analytical Query Engine
        # --------------------------------------------------

        self.query_engine = (
            AnalyticalQueryEngine()
        )


        # --------------------------------------------------
        # Analytics Output Directory
        # --------------------------------------------------

        self.analytics_output_dir = (

            Path(OUTPUT_DIR)

            / "analytics"

        )


        self.analytics_output_dir.mkdir(

            parents=True,

            exist_ok=True

        )


        # --------------------------------------------------
        # Export Audit
        # --------------------------------------------------

        self.export_audit = []


    # ------------------------------------------------------
    # Export One Query Result
    # ------------------------------------------------------

    def export_result(

        self,

        query_name,

        result

    ):

        output_path = (

            self.analytics_output_dir

            / f"{query_name}.csv"

        )


        audit_row = {

            "query_name":
            query_name,

            "output_file":
            str(output_path),

            "rows":
            0,

            "columns":
            0,

            "status":
            "FAILED",

            "error":
            ""

        }


        try:

            # ----------------------------------------------
            # Validate Query Result
            # ----------------------------------------------

            if not isinstance(

                result,

                pd.DataFrame

            ):

                raise TypeError(

                    "Query result must be "
                    "a Pandas DataFrame."

                )


            # ----------------------------------------------
            # Do Not Export Failed or Empty Results
            # ----------------------------------------------

            if result.empty:

                raise ValueError(

                    "Query returned no rows. "
                    "CSV export was skipped."

                )


            # ----------------------------------------------
            # Export Query Result
            # ----------------------------------------------

            result.to_csv(

                output_path,

                index=False

            )


            # ----------------------------------------------
            # Validate Generated File
            # ----------------------------------------------

            if not output_path.exists():

                raise FileNotFoundError(

                    "Analytics CSV file "
                    "was not generated."

                )


            # ----------------------------------------------
            # Update Successful Audit
            # ----------------------------------------------

            audit_row.update(

                {

                    "rows":
                    len(result),

                    "columns":
                    len(
                        result.columns
                    ),

                    "status":
                    "SUCCESS"

                }

            )


            logger.success(

                f"Analytics result "
                f"'{query_name}' exported. "

                f"Rows: {len(result)} | "

                f"Columns: "
                f"{len(result.columns)}"

            )


        except Exception as error:


            audit_row[
                "error"
            ] = str(
                error
            )


            logger.error(

                f"Analytics export "
                f"'{query_name}' failed: "
                f"{error}"

            )


        self.export_audit.append(

            audit_row

        )


        return (

            audit_row[
                "status"
            ]

            == "SUCCESS"

        )


    # ------------------------------------------------------
    # Execute and Export All Financial Queries
    # ------------------------------------------------------

    def run_all(
        self
    ):

        logger.info(

            "Starting predefined "
            "financial analytics..."

        )


        # Clear old audit records before execution

        self.export_audit = []


        self.query_engine.query_audit = []


        # --------------------------------------------------
        # Load All Predefined Queries
        # --------------------------------------------------

        queries = (

            FinancialQueries
            .get_all_queries()

        )


        results = {}


        # --------------------------------------------------
        # Execute Every Query
        # --------------------------------------------------

        for (

            query_name,

            sql_query

        ) in queries.items():


            logger.info(

                f"Executing analytical "
                f"query: {query_name}"

            )


            # ----------------------------------------------
            # Execute Query
            # ----------------------------------------------

            result = (

                self.query_engine
                .execute_query(

                    query_name=

                    query_name,

                    query=

                    sql_query

                )

            )


            # ----------------------------------------------
            # Store Result
            # ----------------------------------------------

            results[

                query_name

            ] = result


            # ----------------------------------------------
            # Export Query Result
            # ----------------------------------------------

            self.export_result(

                query_name=

                query_name,

                result=

                result

            )


        # --------------------------------------------------
        # Export Query Execution Audit
        # --------------------------------------------------

        query_audit = (

            self.query_engine
            .export_audit()

        )


        # --------------------------------------------------
        # Create Analytics Export Manifest
        # --------------------------------------------------

        export_manifest = (

            pd.DataFrame(

                self.export_audit

            )

        )


        manifest_path = (

            OUTPUT_DIR

            / "analytics_export_manifest.csv"

        )


        export_manifest.to_csv(

            manifest_path,

            index=False

        )


        # --------------------------------------------------
        # Calculate Execution Statistics
        # --------------------------------------------------

        total_queries = len(

            queries

        )


        successful_queries = sum(

            1

            for row

            in self.export_audit

            if row[
                "status"
            ] == "SUCCESS"

        )


        failed_queries = (

            total_queries

            - successful_queries

        )


        total_rows_exported = sum(

            row[
                "rows"
            ]

            for row

            in self.export_audit

            if row[
                "status"
            ] == "SUCCESS"

        )


        logger.success(

            "Financial analytics "
            "execution completed."

        )


        # --------------------------------------------------
        # Return Complete Analytics Result
        # --------------------------------------------------

        return {

            "results":

            results,


            "query_audit":

            query_audit,


            "export_manifest":

            export_manifest,


            "total_queries":

            total_queries,


            "successful_queries":

            successful_queries,


            "failed_queries":

            failed_queries,


            "total_rows_exported":

            total_rows_exported,


            "analytics_output_dir":

            self.analytics_output_dir

        }