from pathlib import Path


class PipelineValidator:

    REQUIRED_FILES = [

        "output/analytics/company_financial_snapshot.csv",

        "output/risk/risk_scores.csv",

        "output/portfolio/optimized_portfolio.csv",

        "output/screener/screener_output.csv",

        "output/peer/peer_comparison.csv",

        "output/peer/peer_percentiles.csv",

        "output/sector/sector_summary.csv",

        "output/dashboard/dashboard_dataset.csv",

    ]

    @classmethod
    def validate(cls):

        missing = []

        for file in cls.REQUIRED_FILES:

            if not Path(file).exists():

                missing.append(file)

        return missing