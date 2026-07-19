import pandas as pd


class ForecastPreprocessor:

    @staticmethod
    def prepare(
        df: pd.DataFrame,
        value_column: str,
        company_column: str = "company_id",
        year_column: str = "year",
    ) -> pd.DataFrame:

        data = df.copy()

        data = data[[company_column, year_column, value_column]]

        # Remove rows with missing values first
        data = data.dropna(subset=[company_column, year_column, value_column])

        # Extract a 4-digit year
        data[year_column] = (
            data[year_column]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
        )

        # Drop rows where extraction failed
        data = data.dropna(subset=[year_column])

        # Convert types
        data[year_column] = data[year_column].astype(int)

        data[value_column] = pd.to_numeric(
            data[value_column],
            errors="coerce",
        )

        data = data.dropna(subset=[value_column])

        data = data.sort_values(
            [company_column, year_column]
        )

        return data