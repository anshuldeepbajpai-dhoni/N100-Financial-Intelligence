from dataclasses import dataclass
from typing import Optional


# ==========================================================
# RATIO CALCULATION RESULT
# ==========================================================

@dataclass
class RatioResult:

    value: Optional[float]

    flag: Optional[str] = None

    source_value: Optional[float] = None

    difference: Optional[float] = None


# ==========================================================
# FINANCIAL RATIO ENGINE
# ==========================================================

class FinancialRatioCalculator:

    """
    Provides safe and reusable financial-ratio formulas.

    Day 8:
    - Net Profit Margin
    - Operating Profit Margin
    - OPM source cross-check
    - Return on Equity
    - Return on Capital Employed
    - Return on Assets

    Day 9 leverage and efficiency ratios will be added
    to this class after Day 8 tests pass.
    """


    # ------------------------------------------------------
    # Safe Numeric Conversion
    # ------------------------------------------------------

    @staticmethod
    def _to_float(
        value
    ):

        if value is None:

            return None


        try:

            return float(
                value
            )


        except (
            TypeError,
            ValueError
        ):

            return None


    # ------------------------------------------------------
    # Net Profit Margin
    # ------------------------------------------------------

    @staticmethod
    def net_profit_margin(

        net_profit,

        sales

    ):

        """
        Formula:

        Net Profit Margin
        = Net Profit / Sales × 100

        Returns None when sales is zero,
        missing, or invalid.
        """

        net_profit = (

            FinancialRatioCalculator
            ._to_float(
                net_profit
            )

        )


        sales = (

            FinancialRatioCalculator
            ._to_float(
                sales
            )

        )


        if (

            net_profit is None

            or

            sales is None

            or

            sales == 0

        ):

            return None


        return round(

            (
                net_profit

                / sales
            )

            * 100,

            4

        )


    # ------------------------------------------------------
    # Operating Profit Margin
    # ------------------------------------------------------

    @staticmethod
    def operating_profit_margin(

        operating_profit,

        sales

    ):

        """
        Formula:

        Operating Profit Margin
        = Operating Profit / Sales × 100

        Returns None when sales is zero,
        missing, or invalid.
        """

        operating_profit = (

            FinancialRatioCalculator
            ._to_float(
                operating_profit
            )

        )


        sales = (

            FinancialRatioCalculator
            ._to_float(
                sales
            )

        )


        if (

            operating_profit is None

            or

            sales is None

            or

            sales == 0

        ):

            return None


        return round(

            (
                operating_profit

                / sales
            )

            * 100,

            4

        )


    # ------------------------------------------------------
    # Operating Margin Cross-Check
    # ------------------------------------------------------

    @staticmethod
    def cross_check_operating_margin(

        operating_profit,

        sales,

        source_opm_percentage,

        tolerance=1.0

    ):

        """
        Compares the computed operating-profit margin
        against the source OPM percentage.

        A mismatch is flagged when the absolute
        difference is greater than the tolerance.

        Default tolerance:
        1 percentage point.
        """

        computed_opm = (

            FinancialRatioCalculator
            .operating_profit_margin(

                operating_profit=

                operating_profit,

                sales=

                sales

            )

        )


        source_opm = (

            FinancialRatioCalculator
            ._to_float(

                source_opm_percentage

            )

        )


        if (

            computed_opm is None

            or

            source_opm is None

        ):

            return RatioResult(

                value=

                computed_opm,

                flag=

                "CROSS_CHECK_UNAVAILABLE",

                source_value=

                source_opm,

                difference=

                None

            )


        difference = round(

            abs(

                computed_opm

                - source_opm

            ),

            4

        )


        flag = (

            "OPM_MISMATCH"

            if difference > tolerance

            else

            "MATCH"

        )


        return RatioResult(

            value=

            computed_opm,

            flag=

            flag,

            source_value=

            source_opm,

            difference=

            difference

        )


    # ------------------------------------------------------
    # Return on Equity
    # ------------------------------------------------------

    @staticmethod
    def return_on_equity(

        net_profit,

        equity_capital,

        reserves

    ):

        """
        Formula:

        ROE
        = Net Profit
          / (Equity Capital + Reserves)
          × 100

        Returns None when total shareholder equity
        is zero or negative.
        """

        net_profit = (

            FinancialRatioCalculator
            ._to_float(
                net_profit
            )

        )


        equity_capital = (

            FinancialRatioCalculator
            ._to_float(
                equity_capital
            )

        )


        reserves = (

            FinancialRatioCalculator
            ._to_float(
                reserves
            )

        )


        if (

            net_profit is None

            or

            equity_capital is None

            or

            reserves is None

        ):

            return None


        shareholder_equity = (

            equity_capital

            + reserves

        )


        if shareholder_equity <= 0:

            return None


        return round(

            (
                net_profit

                / shareholder_equity
            )

            * 100,

            4

        )


    # ------------------------------------------------------
    # Return on Capital Employed
    # ------------------------------------------------------

    @staticmethod
    def return_on_capital_employed(

        ebit,

        equity_capital,

        reserves,

        borrowings

    ):

        """
        Formula:

        ROCE
        = EBIT
          / (
              Equity Capital
              + Reserves
              + Borrowings
            )
          × 100

        Returns None when capital employed
        is zero or negative.
        """

        values = [

            ebit,

            equity_capital,

            reserves,

            borrowings

        ]


        converted_values = [

            FinancialRatioCalculator
            ._to_float(
                value
            )

            for value

            in values

        ]


        if any(

            value is None

            for value

            in converted_values

        ):

            return None


        (

            ebit,

            equity_capital,

            reserves,

            borrowings

        ) = converted_values


        capital_employed = (

            equity_capital

            + reserves

            + borrowings

        )


        if capital_employed <= 0:

            return None


        return round(

            (
                ebit

                / capital_employed
            )

            * 100,

            4

        )


    # ------------------------------------------------------
    # Return on Assets
    # ------------------------------------------------------

    @staticmethod
    def return_on_assets(

        net_profit,

        total_assets

    ):

        """
        Formula:

        ROA
        = Net Profit / Total Assets × 100

        Returns None when total assets are zero,
        missing, or invalid.
        """

        net_profit = (

            FinancialRatioCalculator
            ._to_float(
                net_profit
            )

        )


        total_assets = (

            FinancialRatioCalculator
            ._to_float(
                total_assets
            )

        )


        if (

            net_profit is None

            or

            total_assets is None

            or

            total_assets == 0

        ):

            return None


        return round(

            (
                net_profit

                / total_assets
            )

            * 100,

            4

        )


    # ------------------------------------------------------
    # Financial-Sector ROCE Benchmark
    # ------------------------------------------------------

    @staticmethod
    def get_roce_benchmark_type(

        broad_sector

    ):

        """
        Financial-sector companies use a
        sector-relative ROCE benchmark.

        Nonfinancial companies use the
        standard absolute benchmark.
        """

        if broad_sector is None:

            return "ABSOLUTE"


        normalized_sector = (

            str(
                broad_sector
            )
            .strip()
            .lower()

        )


        if normalized_sector == "financials":

            return "SECTOR_RELATIVE"


        return "ABSOLUTE"
    
    # ======================================================
    # DAY 9 — LEVERAGE AND EFFICIENCY RATIOS
    # ======================================================

    # ------------------------------------------------------
    # Debt-to-Equity Ratio
    # ------------------------------------------------------

    @staticmethod
    def debt_to_equity(
        borrowings,
        equity_capital,
        reserves
    ):
        """
        Formula:

        Debt-to-Equity
        = Borrowings
          / (Equity Capital + Reserves)

        Business rules:

        - Returns 0.0 when borrowings are zero.
        - Returns None when shareholder equity is
          zero or negative.
        - Returns None for missing or invalid inputs.
        """

        borrowings = (
            FinancialRatioCalculator
            ._to_float(
                borrowings
            )
        )

        equity_capital = (
            FinancialRatioCalculator
            ._to_float(
                equity_capital
            )
        )

        reserves = (
            FinancialRatioCalculator
            ._to_float(
                reserves
            )
        )

        if (
            borrowings is None
            or equity_capital is None
            or reserves is None
        ):
            return None

        shareholder_equity = (
            equity_capital
            + reserves
        )

        if shareholder_equity <= 0:
            return None

        if borrowings == 0:
            return 0.0

        return round(
            borrowings
            / shareholder_equity,
            4
        )


    # ------------------------------------------------------
    # High-Leverage Flag
    # ------------------------------------------------------

    @staticmethod
    def high_leverage_flag(
        debt_to_equity,
        broad_sector
    ):
        """
        Flags a company when:

        Debt-to-Equity > 5

        Financial-sector companies are excluded because
        high leverage is structurally normal for banks,
        NBFCs, insurers, and similar businesses.
        """

        ratio = (
            FinancialRatioCalculator
            ._to_float(
                debt_to_equity
            )
        )

        if ratio is None:
            return False

        normalized_sector = (
            str(
                broad_sector
            )
            .strip()
            .lower()
            if broad_sector is not None
            else ""
        )

        if normalized_sector == "financials":
            return False

        return ratio > 5


    # ------------------------------------------------------
    # Interest Coverage Ratio
    # ------------------------------------------------------

    @staticmethod
    def interest_coverage_ratio(
        operating_profit,
        other_income,
        interest
    ):
        """
        Formula:

        Interest Coverage Ratio
        = (
            Operating Profit
            + Other Income
          )
          / Interest

        Returns None when interest is zero.

        A zero-interest company is treated as debt-free
        for display purposes.
        """

        operating_profit = (
            FinancialRatioCalculator
            ._to_float(
                operating_profit
            )
        )

        other_income = (
            FinancialRatioCalculator
            ._to_float(
                other_income
            )
        )

        interest = (
            FinancialRatioCalculator
            ._to_float(
                interest
            )
        )

        if (
            operating_profit is None
            or other_income is None
            or interest is None
        ):
            return None

        if interest == 0:
            return None

        return round(
            (
                operating_profit
                + other_income
            )
            / interest,
            4
        )


    # ------------------------------------------------------
    # Interest-Coverage Display Label
    # ------------------------------------------------------

    @staticmethod
    def interest_coverage_label(
        interest_coverage,
        interest
    ):
        """
        Returns:

        Debt Free
            when interest is zero.

        Not Available
            when ICR cannot be calculated for another
            reason.

        Covered
            when ICR is at least 1.5.

        At Risk
            when ICR is below 1.5.
        """

        interest = (
            FinancialRatioCalculator
            ._to_float(
                interest
            )
        )

        ratio = (
            FinancialRatioCalculator
            ._to_float(
                interest_coverage
            )
        )

        if interest == 0:
            return "Debt Free"

        if ratio is None:
            return "Not Available"

        if ratio < 1.5:
            return "At Risk"

        return "Covered"


    # ------------------------------------------------------
    # Interest-Coverage Warning
    # ------------------------------------------------------

    @staticmethod
    def interest_coverage_warning(
        interest_coverage
    ):
        """
        Returns True when ICR is below 1.5.

        None values are not flagged because zero-interest
        companies are handled separately as debt-free.
        """

        ratio = (
            FinancialRatioCalculator
            ._to_float(
                interest_coverage
            )
        )

        if ratio is None:
            return False

        return ratio < 1.5


    # ------------------------------------------------------
    # Net Debt
    # ------------------------------------------------------

    @staticmethod
    def net_debt(
        borrowings,
        investments
    ):
        """
        Formula:

        Net Debt
        = Borrowings - Investments

        Investments are used as the liquid-asset proxy.

        Negative net debt is valid and indicates that
        investments exceed borrowings.
        """

        borrowings = (
            FinancialRatioCalculator
            ._to_float(
                borrowings
            )
        )

        investments = (
            FinancialRatioCalculator
            ._to_float(
                investments
            )
        )

        if (
            borrowings is None
            or investments is None
        ):
            return None

        return round(
            borrowings
            - investments,
            4
        )


    # ------------------------------------------------------
    # Asset Turnover
    # ------------------------------------------------------

    @staticmethod
    def asset_turnover(
        sales,
        total_assets
    ):
        """
        Formula:

        Asset Turnover
        = Sales / Total Assets

        Returns None when total assets are zero.
        """

        sales = (
            FinancialRatioCalculator
            ._to_float(
                sales
            )
        )

        total_assets = (
            FinancialRatioCalculator
            ._to_float(
                total_assets
            )
        )

        if (
            sales is None
            or total_assets is None
            or total_assets == 0
        ):
            return None

        return round(
            sales
            / total_assets,
            4
        )