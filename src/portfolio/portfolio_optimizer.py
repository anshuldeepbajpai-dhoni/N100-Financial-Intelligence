class PortfolioOptimizer:

    @staticmethod
    def optimize(df, top_n=20):

        return (

            df

            .sort_values(

                "portfolio_score",

                ascending=False,

            )

            .head(top_n)

            .reset_index(drop=True)

        )