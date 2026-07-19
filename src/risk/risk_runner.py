from .risk_scoring import RiskScorer
from .risk_summary import RiskSummary
from .export import RiskExporter


class RiskRunner:

    def run(self, portfolio):

        scores = RiskScorer.calculate(

            portfolio

        )

        summary = RiskSummary.generate(

            scores

        )

        RiskExporter.save(

            scores,

            summary,

        )

        print("\nRisk Analytics Completed.\n")

        return scores