import pandas as pd

from src.etl.normalizer import DataNormalizer


def test_column_normalization():

    df = pd.DataFrame({

        "Company ID": ["ABC"]

    })

    df = DataNormalizer.normalize_columns(df)

    assert "company_id" in df.columns


def test_remove_duplicates():

    df = pd.DataFrame({

        "id": [1, 1]

    })

    df = DataNormalizer.remove_duplicates(df)

    assert len(df) == 1