from .engine import SectorEngine
from .export import SectorExporter


class SectorRunner:

    def __init__(self):

        self.engine = SectorEngine()

    def run(self, analytics_result):

        snapshot = analytics_result["results"]["company_financial_snapshot"]

        results = self.engine.analyze(snapshot)

        SectorExporter.save_all(results)

        print("\nSector Analytics Completed.\n")

        return results