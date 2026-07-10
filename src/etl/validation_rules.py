import re
import pandas as pd


class ValidationRules:
    """
    Collection of reusable Data Quality validation rules.
    """

    @staticmethod
    def check_primary_key(df: pd.DataFrame, key: str) -> pd.DataFrame:
        """DQ-01"""
        if key not in df.columns:
            return pd.DataFrame()

        return df[df.duplicated(subset=[key], keep=False)]

    @staticmethod
    def check_composite_key(df: pd.DataFrame,
                            keys: list) -> pd.DataFrame:
        """DQ-02"""

        if not all(col in df.columns for col in keys):
            return pd.DataFrame()

        return df[df.duplicated(subset=keys, keep=False)]

    @staticmethod
    def check_foreign_key(df,
                          fk_column,
                          master_df,
                          master_key):

        """DQ-03"""

        if fk_column not in df.columns:
            return pd.DataFrame()

        if master_key not in master_df.columns:
            return pd.DataFrame()

        master = (
            master_df[master_key]
            .astype(str)
            .str.upper()
            .str.strip()
            .str.replace("-", "", regex=False)
            .str.replace(" ", "", regex=False)
        )

        child = (
            df[fk_column]
            .astype(str)
            .str.upper()
            .str.strip()
            .str.replace("-", "", regex=False)
            .str.replace(" ", "", regex=False)
        )

        return df[~child.isin(master)]

    @staticmethod
    def check_duplicate_rows(df):

        """DQ-04"""

        return df[df.duplicated(keep=False)]

    @staticmethod
    def check_mandatory_fields(df,
                               columns):

        """DQ-05"""

        cols = [
            c for c in columns
            if c in df.columns
        ]

        if not cols:
            return pd.DataFrame()

        return df[
            df[cols]
            .isna()
            .any(axis=1)
        ]
    
    @staticmethod
    def check_positive_sales(df):

        """DQ-06"""

        if "sales" not in df.columns:
            return pd.DataFrame()

        return df[
            df["sales"] <= 0
        ]
    @staticmethod

    def check_operating_profit(
        df: pd.DataFrame,
        tolerance: float = 1.0
    ) -> pd.DataFrame:
        """
        DQ-07:
        Cross-check reported OPM percentage.

        Calculated OPM:
        (operating_profit / sales) * 100

        The tolerance is measured in percentage points.
        """

        required = [
            "sales",
            "operating_profit",
            "opm_percentage"
        ]

        if not all(
            column in df.columns
            for column in required
        ):
            return pd.DataFrame()

        working = df.copy()

        for column in required:
            working[column] = pd.to_numeric(
                working[column],
                errors="coerce"
            )

        valid_mask = (
            working["sales"].notna()
            & working["operating_profit"].notna()
            & working["opm_percentage"].notna()
            & (working["sales"] != 0)
        )

        calculated_opm = (
            working["operating_profit"]
            / working["sales"]
        ) * 100

        difference = (
            calculated_opm
            - working["opm_percentage"]
        ).abs()

        invalid_mask = (
            valid_mask
            & (difference > tolerance)
        )

        return df[invalid_mask]

    @staticmethod
    def check_balance_sheet(df,
                            tolerance):

        """DQ-08"""

        required = [
            "total_assets",
            "total_liabilities"
        ]

        if not all(col in df.columns for col in required):
            return pd.DataFrame()

        diff = abs(
            df["total_assets"] -
            df["total_liabilities"]
        )

        return df[
            diff >
            abs(df["total_assets"]) * tolerance
        ]

    @staticmethod
    def check_cash_flow(
        df: pd.DataFrame,
        tolerance: float
    ) -> pd.DataFrame:
        """
        DQ-09:
        Net cash flow should approximately equal:

        operating activity
        + investing activity
        + financing activity

        A minimum absolute tolerance is used for
        small and zero expected values.
        """

        required = [
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow"
        ]

        if not all(
            column in df.columns
            for column in required
        ):
            return pd.DataFrame()

        working = df.copy()

        for column in required:

            working[column] = pd.to_numeric(
                working[column],
                errors="coerce"
            )

        expected = (
            working["operating_activity"]
            + working["investing_activity"]
            + working["financing_activity"]
        )

        difference = (
            working["net_cash_flow"] - expected
        ).abs()

        allowed_difference = (
            expected.abs() * tolerance
        ).clip(lower=1.0)

        invalid_mask = (
            difference > allowed_difference
        )

        return df[invalid_mask]
    
    @staticmethod
    def check_tax_rate(
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        DQ-10:
        Flag extreme effective tax percentages.

        Negative values are allowed because tax credits
        and deferred-tax adjustments can occur.
        """

        if "tax_percentage" not in df.columns:
            return pd.DataFrame()

        tax_rate = pd.to_numeric(
            df["tax_percentage"],
            errors="coerce"
        )

        invalid_mask = (
            tax_rate.notna()
            & (
                (tax_rate < -100)
                | (tax_rate > 100)
            )
        )

        return df[invalid_mask]

    @staticmethod
    def check_dividend(
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        DQ-11:
        Validate dividend payout percentage.

        Negative values and values above 100%
        are reported as warnings.
        """

        if "dividend_payout" not in df.columns:
            return pd.DataFrame()

        dividend = pd.to_numeric(
            df["dividend_payout"],
            errors="coerce"
        )

        invalid_mask = (
            dividend.notna()
            & (
                (dividend < 0)
                | (dividend > 100)
            )
        )

        return df[invalid_mask]

    @staticmethod
    def check_eps(df):

        required = [
            "eps",
            "net_profit"
        ]

        if not all(c in df.columns for c in required):
            return pd.DataFrame()

        return df[
            (
                (df["net_profit"] > 0) &
                (df["eps"] < 0)
            )
            |
            (
                (df["net_profit"] < 0) &
                (df["eps"] > 0)
            )
        ]


    @staticmethod
    def check_url(df):

        import re

        url_cols = [
            c for c in df.columns
            if "url" in c.lower()
            or "website" in c.lower()
        ]

        if not url_cols:
            return pd.DataFrame()

        pattern = re.compile(r"^https?://")

        invalid = pd.DataFrame()

        for col in url_cols:

            temp = df[
                ~df[col]
                .fillna("")
                .astype(str)
                .str.match(pattern)
            ]

            invalid = pd.concat(
                [invalid, temp]
            )

        return invalid.drop_duplicates()


    @staticmethod
    def check_year(
        df: pd.DataFrame,
        minimum_year: int = 2000,
        maximum_year: int = 2035
    ) -> pd.DataFrame:
        """
        DQ-14:
        Validate financial year values.

        Missing or non-numeric years are invalid.
        """

        if "year" not in df.columns:
            return pd.DataFrame()

        years = pd.to_numeric(
            df["year"],
            errors="coerce"
        )

        invalid_mask = (
            years.isna()
            | (years < minimum_year)
            | (years > maximum_year)
        )

        return df[invalid_mask]

    @staticmethod
    def check_numeric(df, numeric_columns):

        if not numeric_columns:
            return pd.DataFrame()

        invalid = pd.DataFrame()

        for col in numeric_columns:

            if col not in df.columns:
                continue

            bad = df[
                pd.to_numeric(
                    df[col],
                    errors="coerce"
                ).isna()
                &
                df[col].notna()
            ]

            invalid = pd.concat(
                [invalid, bad]
            )

        return invalid.drop_duplicates()

    @staticmethod
    def check_company_coverage(df):

        if "company_id" not in df.columns:
            return pd.DataFrame()

        counts = df.groupby("company_id").size()

        missing = counts[counts < 1]

        if missing.empty:
            return pd.DataFrame()

        return df[
            df["company_id"].isin(
                missing.index
            )
        ]