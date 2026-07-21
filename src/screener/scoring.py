import numpy as np


def add_placeholder_score(df):
    """
    Day 17 replaces this with
    Composite Quality Score.
    """

    df = df.copy()

    df["composite_quality_score"] = np.nan

    return df