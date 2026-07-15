import re

import pandas as pd

from src.etl.logger import logger


# ==========================================================
# DATABASE SCHEMA MANAGER
# ==========================================================

class DatabaseSchema:

    """
    Generates SQLite-compatible table names and
    SQL column definitions from processed DataFrames.
    """

    # ------------------------------------------------------
    # Normalize SQL Table Name
    # ------------------------------------------------------

    @staticmethod
    def normalize_table_name(
        dataset_name
    ):

        table_name = str(
            dataset_name
        ).strip().lower()

        # Remove file extension
        table_name = re.sub(
            r"\.(xlsx|xls|csv)$",
            "",
            table_name
        )

        # Replace unsupported characters
        table_name = re.sub(
            r"[^a-z0-9_]+",
            "_",
            table_name
        )

        # Remove unnecessary underscores
        table_name = table_name.strip(
            "_"
        )

        return table_name


    # ------------------------------------------------------
    # Convert Pandas Type to SQLite Type
    # ------------------------------------------------------

    @staticmethod
    def get_sqlite_type(
        series
    ):

        if pd.api.types.is_integer_dtype(
            series
        ):

            return "INTEGER"

        if pd.api.types.is_float_dtype(
            series
        ):

            return "REAL"

        if pd.api.types.is_bool_dtype(
            series
        ):

            return "INTEGER"

        if pd.api.types.is_datetime64_any_dtype(
            series
        ):

            return "TEXT"

        return "TEXT"


    # ------------------------------------------------------
    # Generate SQL Column Definitions
    # ------------------------------------------------------

    @classmethod
    def generate_columns(
        cls,
        dataframe
    ):

        columns = []

        for column in dataframe.columns:

            sql_type = cls.get_sqlite_type(
                dataframe[column]
            )

            column_definition = (

                f'"{column}" '
                f"{sql_type}"

            )

            columns.append(
                column_definition
            )

        return columns


    # ------------------------------------------------------
    # Generate CREATE TABLE Query
    # ------------------------------------------------------

    @classmethod
    def generate_create_table_query(
        cls,
        table_name,
        dataframe
    ):

        if dataframe is None:

            raise ValueError(
                "DataFrame cannot be None."
            )

        if dataframe.empty:

            logger.warning(

                f"{table_name}: "
                "DataFrame is empty."

            )

        normalized_table_name = (
            cls.normalize_table_name(
                table_name
            )
        )

        columns = cls.generate_columns(
            dataframe
        )

        if not columns:

            raise ValueError(

                f"{table_name}: "
                "No database columns found."

            )

        column_sql = ",\n    ".join(
            columns
        )

        query = f"""
CREATE TABLE IF NOT EXISTS
"{normalized_table_name}"
(
    {column_sql}
);
"""

        return query