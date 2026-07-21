from .scoring import PortfolioScorer
from .portfolio_optimizer import PortfolioOptimizer
from .export import PortfolioExporter
from .sector_allocator import SectorAllocator
from .allocation import PortfolioAllocation
from pathlib import Path


class PortfolioRunner:

    def run(self, analytics_result):

        snapshot = analytics_result["results"]["company_financial_snapshot"]

        scored = PortfolioScorer.score(snapshot)

        portfolio = PortfolioOptimizer.optimize(
            scored,
            top_n=50
        )

        portfolio = SectorAllocator.diversify(
            portfolio,
            max_per_sector=3
        )
        
        portfolio = PortfolioAllocation.calculate(
            portfolio
        )

        print(portfolio.columns.tolist())
        print(portfolio.head())

        PortfolioExporter.save(portfolio)

        # ----------------------------------------
        # Sector Allocation
        # ----------------------------------------

        sector_allocation = (

            portfolio

            .groupby("broad_sector")

            .agg(

                companies=("company_name", "count"),

                total_weight=("allocation_percent", "sum")

            )

            .reset_index()

        )

        output = Path("output") / "portfolio"
        output.mkdir(parents=True, exist_ok=True)

        sector_allocation.to_csv(

            output / "sector_allocation.csv",

            index=False

        )

        print("\nPortfolio Optimization Completed\n")

        return portfolio