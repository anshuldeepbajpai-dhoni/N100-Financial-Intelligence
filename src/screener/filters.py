import numpy as np
import pandas as pd


def min_filter(df, column, value):
    return df[df[column] >= value]


def max_filter(df, column, value):
    return df[df[column] <= value]


def debt_equity_filter(df, column, threshold):
    """
    Ignore Debt/Equity filter for Financial sector companies.
    """

    financial_mask = (
        df["broad_sector"]
        .astype(str)
        .str.lower()
        == "financials"
    )

    financial_df = df[financial_mask]

    non_financial = df[~financial_mask]

    filtered = non_financial[
        non_financial[column] <= threshold
    ]

    return (
        pd.concat(
            [filtered, financial_df],
            ignore_index=True
        )
    )


def interest_coverage_filter(
    df,
    column,
    threshold
):
    """
    Debt Free -> Infinity
    """

    temp = df.copy()

    temp[column] = (
        temp[column]
        .replace(
            "Debt Free",
            np.inf
        )
    )

    temp[column] = pd.to_numeric(
        temp[column],
        errors="coerce"
    )

    return temp[
        temp[column] >= threshold
    ]