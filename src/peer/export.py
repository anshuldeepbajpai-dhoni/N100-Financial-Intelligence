from pathlib import Path


class PeerExporter:

    OUTPUT = Path("output") / "peer"

    @classmethod
    def save_all(cls, results):

        cls.OUTPUT.mkdir(
            parents=True,
            exist_ok=True,
        )

        results["peer_comparison"].to_csv(
            cls.OUTPUT / "peer_comparison.csv",
            index=False,
        )

        results["peer_comparison"].to_csv(
            cls.OUTPUT / "peer_rankings.csv",
            index=False,
        )

        results["peer_summary"].to_csv(
            cls.OUTPUT / "peer_summary.csv",
            index=False,
        )

        print("\nPeer Comparison Exported.")