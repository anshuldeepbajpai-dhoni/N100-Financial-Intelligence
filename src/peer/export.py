from pathlib import Path


class PeerExporter:

    OUTPUT = Path("output") / "peer"

    @classmethod
    def save_all(cls, results):

        cls.OUTPUT.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Complete comparison with percentile columns
        results["peer_comparison"].to_csv(
            cls.OUTPUT / "peer_comparison.csv",
            index=False,
        )

        # Rankings
        results["peer_comparison"].to_csv(
            cls.OUTPUT / "peer_rankings.csv",
            index=False,
        )

        # NEW: Percentile output
        results["peer_comparison"].to_csv(
            cls.OUTPUT / "peer_percentiles.csv",
            index=False,
        )

        # Sector summary
        results["peer_summary"].to_csv(
            cls.OUTPUT / "peer_summary.csv",
            index=False,
        )

        print("\nPeer Comparison Exported Successfully.")