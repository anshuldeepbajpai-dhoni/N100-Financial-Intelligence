import pandas as pd
import re

class DataNormalizer:

    @staticmethod
    def normalize_columns(df: pd.DataFrame):

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )

        return df

    @staticmethod
    def normalize_company_id(df):

        columns = ["id", "company_id"]

        for col in columns:

            if col in df.columns:

                df[col] = (
                    df[col]
                    .astype(str)
                    .str.upper()
                    .str.strip()
                    .str.replace(" ", "", regex=False)
                    .str.replace("-", "", regex=False)
                    .str.replace("&", "AND", regex=False)
                )

        return df

    @staticmethod
    def normalize_year(value):
        """
        Normalize financial-year values.

        Examples:
        2024        -> 2024
        2024.0      -> 2024
        "2023-24"   -> 2024
        "Mar 2024"  -> 2024
        "FY24"      -> 2024

        Missing or invalid values remain None.
        """

        if pd.isna(value):
            return None

        value = str(value).strip()

        if value == "":
            return None

        # Normal four-digit year
        match = re.search(
            r"\b(19\d{2}|20\d{2})\b",
            value
        )

        if match:
            return int(match.group(1))

        # FY24, FY25, etc.
        match = re.search(
            r"FY\s*(\d{2})",
            value,
            re.IGNORECASE
        )

        if match:

            short_year = int(
                match.group(1)
            )

            return (
                2000 + short_year
                if short_year < 50
                else 1900 + short_year
            )

        return None

    @staticmethod
    def remove_duplicates(df):

        return df.drop_duplicates()

    @staticmethod
    def clean(df):

        df = DataNormalizer.normalize_columns(df)
        df = DataNormalizer.normalize_company_id(df)
        df = DataNormalizer.normalize_year(df)
        df = DataNormalizer.remove_duplicates(df)

        return df