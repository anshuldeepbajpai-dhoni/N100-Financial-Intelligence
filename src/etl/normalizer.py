import pandas as pd


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

        if "company_id" in df.columns:

            df["company_id"] = (
                df["company_id"]
                .astype(str)
                .str.strip()
                .str.upper()
            )

        if "id" in df.columns:

            df["id"] = (
                df["id"]
                .astype(str)
                .str.strip()
                .str.upper()
            )

        return df

    @staticmethod
    def normalize_year(df):

        if "year" in df.columns:

            df["year"] = (
                pd.to_datetime(
                    df["year"],
                    errors="coerce"
                )
                .dt.year
            )

        return df

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