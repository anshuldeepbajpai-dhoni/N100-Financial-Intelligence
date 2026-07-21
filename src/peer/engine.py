from .ranking import PeerRanking


class PeerEngine:

    def compare(self, snapshot):

        ranked = PeerRanking.rank(snapshot)

        summary = (
            ranked
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

            "peer_comparison": ranked,

            "peer_summary": summary,

        }