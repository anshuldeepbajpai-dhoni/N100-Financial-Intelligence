from .engine import PeerEngine
from .export import PeerExporter


class PeerRunner:

    def __init__(self):

        self.engine = PeerEngine()

    def run(self, analytics_result):

        snapshot = analytics_result["results"]["company_financial_snapshot"]

        results = self.engine.compare(snapshot)

        PeerExporter.save_all(results)

        print("\nPeer Comparison Completed.\n")

        return results