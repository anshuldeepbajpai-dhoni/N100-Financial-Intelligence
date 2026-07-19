from .scoring import PortfolioScorer
from .portfolio_optimizer import PortfolioOptimizer
from .export import PortfolioExporter
from .sector_allocator import SectorAllocator
from .allocation import PortfolioAllocation


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

        PortfolioExporter.save(portfolio)

        print("\nPortfolio Optimization Completed\n")

        return portfolio