from .builder import DashboardBuilder
from .export import DashboardExporter


class DashboardRunner:

    def __init__(self):

        self.builder = DashboardBuilder()

    def run(

        self,

        analytics_result,

        peer_result,

        sector_result,

        portfolio_result,

        risk_result

    ):

        dataset = self.builder.build(

            analytics_result,

            peer_result,

            sector_result,

            portfolio_result,

            risk_result

        )

        DashboardExporter.save(dataset)

        print("Dashboard Dataset Generated.\n")

        return dataset