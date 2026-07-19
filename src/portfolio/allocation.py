class PortfolioAllocation:

    @staticmethod
    def calculate(df):

        portfolio = df.copy()

        total = portfolio["portfolio_score"].sum()

        portfolio["allocation_percent"] = (

            portfolio["portfolio_score"]

            / total

        ) * 100

        return portfolio