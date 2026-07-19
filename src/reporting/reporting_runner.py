from .executive_summary import ExecutiveSummary

from .dashboard_dataset import DashboardDataset

from .export import ReportExporter


class ReportingRunner:

    def run(

        self,

        analytics_result,

        portfolio_result,

        risk_result,

    ):

        summary = ExecutiveSummary.generate(

            analytics_result,

            portfolio_result,

            risk_result,

        )

        dashboard = DashboardDataset.generate(

            portfolio_result,

            risk_result,

        )

        ReportExporter.save(

            summary,

            dashboard,

        )

        print(

            "\nExecutive Reporting Completed.\n"

        )

        return {

            "summary": summary,

            "dashboard": dashboard,

        }