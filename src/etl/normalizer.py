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
        Convert financial-period labels into integer years.

        Examples:
        Mar 2024      -> 2024
        Dec 2012      -> 2012
        Mar-24        -> 2024
        Mar 2023 15   -> 2023
        Mar 2016 9m   -> 2016
        FY24          -> 2024
        FY2024        -> 2024
        2023-24       -> 2024
        TTM           -> NA
        """

        if pd.isna(value):
            return pd.NA

        # ---------------------------------------------
        # Existing numeric values
        # ---------------------------------------------

        if isinstance(value, (int, float)):

            year = int(value)

            return year

        # ---------------------------------------------
        # Clean string
        # ---------------------------------------------

        text = str(value).strip()

        if not text:
            return pd.NA

        # ---------------------------------------------
        # Non-annual financial periods
        # ---------------------------------------------

        if text.upper() in {
            "TTM",
            "LTM",
            "N/A",
            "NA",
            "NONE",
            "NAN"
        }:
            return pd.NA

        # ---------------------------------------------
        # Find a four-digit year anywhere
        #
        # Mar 2024      -> 2024
        # Dec 2012      -> 2012
        # Mar 2023 15   -> 2023
        # Mar 2016 9m   -> 2016
        # ---------------------------------------------

        four_digit_year = re.search(
            r"\b(19\d{2}|20\d{2}|21\d{2})\b",
            text
        )

        if four_digit_year:

            return int(
                four_digit_year.group(1)
            )

        # ---------------------------------------------
        # Month-short-year format
        #
        # Mar-24 -> 2024
        # Dec-13 -> 2013
        # ---------------------------------------------

        month_short_year = re.search(
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|"
            r"Sep|Oct|Nov|Dec)"
            r"[\s\-/]+(\d{2})\b",
            text,
            flags=re.IGNORECASE
        )

        if month_short_year:

            short_year = int(
                month_short_year.group(1)
            )

            if short_year <= 50:
                return 2000 + short_year

            return 1900 + short_year

        # ---------------------------------------------
        # FY short-year format
        #
        # FY24 -> 2024
        # ---------------------------------------------

        fy_short_year = re.search(
            r"\bFY[\s\-/]*(\d{2})\b",
            text,
            flags=re.IGNORECASE
        )

        if fy_short_year:

            short_year = int(
                fy_short_year.group(1)
            )

            if short_year <= 50:
                return 2000 + short_year

            return 1900 + short_year

        # ---------------------------------------------
        # Unrecognized values remain missing
        # ---------------------------------------------

        return pd.NA

    @staticmethod
    def remove_exact_duplicates(df):
        """
        Remove exact duplicate records while ignoring
        the artificial row ID.

        Records with the same company_id and year but
        different financial values are preserved.
        """

        if df is None or df.empty:

            return df

        # Compare all columns except artificial ID
        comparison_columns = [
            column
            for column in df.columns
            if column != "id"
        ]

        if not comparison_columns:

            return df

        rows_before = len(df)

        # Keep the first occurrence of an exact record
        df = df.drop_duplicates(
            subset=comparison_columns,
            keep="first"
        ).copy()

        rows_removed = (
            rows_before - len(df)
        )

        return df
    

    @staticmethod
    def normalize_reporting_period(value):
        """
        Standardize source financial-period labels.

        Examples:
        Mar-24       -> MAR-2024
        Mar 2024     -> MAR-2024
        Dec 2012     -> DEC-2012
        Sep 2024     -> SEP-2024
        TTM          -> TTM
        """

        if pd.isna(value):

            return pd.NA

        text = str(value).strip()

        if not text:

            return pd.NA

        if text.upper() in {
            "TTM",
            "LTM"
        }:

            return text.upper()

        month_match = re.search(
            r"\b"
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|"
            r"Sep|Oct|Nov|Dec)"
            r"[\s\-/]+"
            r"(\d{2}|\d{4})"
            r"\b",
            text,
            flags=re.IGNORECASE
        )

        if month_match:

            month = (
                month_match
                .group(1)
                .upper()
            )

            year = int(
                month_match.group(2)
            )

            if year < 100:

                if year <= 50:

                    year = 2000 + year

                else:

                    year = 1900 + year

            return f"{month}-{year}"

        return text.upper()


    @staticmethod
    def clean(df):

        if df is None:

            return pd.DataFrame()

        df = df.copy()

        # --------------------------------------------------
        # Clean Column Names
        # --------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(
                " ",
                "_",
                regex=False
            )
            .str.replace(
                "-",
                "_",
                regex=False
            )
        )

        # --------------------------------------------------
        # Remove Completely Empty Rows
        # --------------------------------------------------

        df = df.dropna(
            how="all"
        )

        # --------------------------------------------------
        # Normalize Company ID
        # --------------------------------------------------

        if "company_id" in df.columns:

            df["company_id"] = (
                df["company_id"]
                .astype("string")
                .str.strip()
                .str.upper()
            )

        # --------------------------------------------------
        # Preserve Original Financial Period
        # --------------------------------------------------

        if "year" in df.columns:

            # Preserve the original source period before
            # extracting the normalized financial year.
            df["reporting_period"] = (
                df["year"]
                .astype("string")
                .str.strip()
            )

            # Extract normalized integer year.
            df["year"] = (
                df["year"]
                .apply(
                    DataNormalizer.normalize_year
                )
                .astype("Int64")
            )

        # --------------------------------------------------
        # Normalize Financial Period and Year
        # --------------------------------------------------

        if "year" in df.columns:

            original_year = (
                df["year"]
                .copy()
            )

            df["reporting_period"] = (
                original_year
                .apply(
                    DataNormalizer
                    .normalize_reporting_period
                )
                .astype("string")
            )

            df["year"] = (
                original_year
                .apply(
                    DataNormalizer.normalize_year
                )
                .astype("Int64")
            )

        # --------------------------------------------------
        # Remove Exact Duplicate Records
        # --------------------------------------------------

        df = DataNormalizer.remove_exact_duplicates(
            df
        )

        # --------------------------------------------------
        # Reset Index
        # --------------------------------------------------

        df = df.reset_index(
            drop=True
        )

        return df