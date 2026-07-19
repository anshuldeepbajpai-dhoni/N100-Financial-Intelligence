import pandas as pd


class SectorAllocator:

    @staticmethod
    def diversify(df, max_per_sector=3):

        diversified = (

            df

            .groupby("broad_sector", group_keys=False)

            .head(max_per_sector)

            .reset_index(drop=True)

        )

        return diversified