from .ranking import PeerRanking
from .percentile import PeerPercentile

class PeerEngine:

    def compare(self, snapshot):

        ranked = PeerRanking.rank(snapshot)

        percentiles = PeerPercentile.calculate(ranked)

        summary = (
            percentiles
            .groupby("broad_sector")
            .agg(
                companies=("company_name", "count"),
                avg_roe=("roe_percentage", "mean"),
                avg_roce=("roce_percentage", "mean"),
                avg_opm=("opm_percentage", "mean"),
            )
            .reset_index()
        )

        return {

            "peer_comparison": percentiles,

            "peer_summary": summary,

        }