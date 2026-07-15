import time

import pandas as pd

from src.database.connection import (
    DatabaseConnection
)

from src.database.schema import (
    DatabaseSchema
)

from src.etl.config import (
    OUTPUT_DIR
)

from src.etl.logger import (
    logger
)


# ==========================================================
# SQLITE DATABASE LOADER
# ==========================================================

class DatabaseLoader:

    """
    Loads processed DataFrames into SQLite and
    generates a database load audit.
    """

    def __init__(
        self
    ):

        self.database = (
            DatabaseConnection()
        )

        self.load_audit = []


    # ------------------------------------------------------
    # Load One DataFrame
    # ------------------------------------------------------

    def load_dataset(
        self,
        dataset_name,
        dataframe
    ):

        start_time = time.perf_counter()

        table_name = (
            DatabaseSchema
            .normalize_table_name(
                dataset_name
            )
        )

        audit_row = {

            "dataset": dataset_name,

            "table_name": table_name,

            "source_rows": 0,

            "database_rows": 0,

            "columns": 0,

            "duration_seconds": 0,

            "status": "FAILED",

            "error": ""

        }


        try:

            if dataframe is None:

                raise ValueError(

                    "DataFrame is None."

                )


            audit_row[
                "source_rows"
            ] = len(
                dataframe
            )


            audit_row[
                "columns"
            ] = len(
                dataframe.columns
            )


            if len(
                dataframe.columns
            ) == 0:

                raise ValueError(

                    "DataFrame contains "
                    "no columns."

                )


            with (
                self.database
                .transaction()
            ) as connection:


                # ------------------------------------------
                # Replace existing table safely
                # ------------------------------------------

                connection.execute(

                    f'DROP TABLE IF EXISTS '
                    f'"{table_name}";'

                )


                # ------------------------------------------
                # Generate and execute schema
                # ------------------------------------------

                create_query = (

                    DatabaseSchema
                    .generate_create_table_query(

                        table_name,

                        dataframe

                    )

                )


                connection.execute(
                    create_query
                )


                # ------------------------------------------
                # Insert DataFrame records
                # ------------------------------------------

                dataframe.to_sql(

                    name=table_name,

                    con=connection,

                    if_exists="append",

                    index=False

                )


                # ------------------------------------------
                # Verify database row count
                # ------------------------------------------

                result = (
                    connection.execute(

                        f"""
                        SELECT COUNT(*)
                        FROM "{table_name}";
                        """

                    ).fetchone()
                )


                database_rows = int(
                    result[0]
                )


                audit_row[
                    "database_rows"
                ] = database_rows


                # ------------------------------------------
                # Detect silent row loss
                # ------------------------------------------

                if (

                    database_rows

                    !=

                    len(dataframe)

                ):

                    raise ValueError(

                        "Database row-count "
                        "verification failed. "

                        f"Source: "
                        f"{len(dataframe)}, "

                        f"Database: "
                        f"{database_rows}"

                    )


            audit_row[
                "status"
            ] = "SUCCESS"


            logger.success(

                f"{dataset_name} loaded into "

                f"SQLite table "
                f"'{table_name}'."

            )


        except Exception as error:

            audit_row[
                "error"
            ] = str(
                error
            )


            logger.error(

                f"{dataset_name} database "

                f"load failed: {error}"

            )


        finally:

            audit_row[
                "duration_seconds"
            ] = round(

                time.perf_counter()

                - start_time,

                4

            )


            self.load_audit.append(
                audit_row
            )


        return (

            audit_row["status"]

            == "SUCCESS"

        )


    # ------------------------------------------------------
    # Load All Datasets
    # ------------------------------------------------------

    def load_all(
        self,
        datasets
    ):

        logger.info(

            "Starting processed-data "
            "database loading..."

        )


        successful_tables = []


        for (

            dataset_name,

            dataframe

        ) in datasets.items():


            success = self.load_dataset(

                dataset_name,

                dataframe

            )


            if success:

                successful_tables.append(

                    DatabaseSchema
                    .normalize_table_name(

                        dataset_name

                    )

                )


        self.generate_load_audit()


        logger.success(

            "Processed-data database "
            "loading completed."

        )


        return successful_tables


    # ------------------------------------------------------
    # Generate Database Load Audit
    # ------------------------------------------------------

    def generate_load_audit(
        self
    ):

        audit_report = pd.DataFrame(

            self.load_audit

        )


        output_path = (

            OUTPUT_DIR

            / "database_load_audit.csv"

        )


        audit_report.to_csv(

            output_path,

            index=False

        )


        logger.success(

            "Database load audit saved to "

            f"{output_path}"

        )


        return audit_report