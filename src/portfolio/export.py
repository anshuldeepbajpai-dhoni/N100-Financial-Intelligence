from pathlib import Path


class PortfolioExporter:

    OUTPUT = Path("output/portfolio")

    @classmethod
    def save(cls, df):

        cls.OUTPUT.mkdir(

            parents=True,

            exist_ok=True,

        )

        df.to_csv(

            cls.OUTPUT /

            "optimized_portfolio.csv",

            index=False,

        )

        print("Portfolio exported.")