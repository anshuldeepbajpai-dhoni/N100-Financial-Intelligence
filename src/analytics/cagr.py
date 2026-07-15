from dataclasses import dataclass
from typing import Optional, Sequence


# ==========================================================
# CAGR RESULT
# ==========================================================

@dataclass
class CAGRResult:
    """
    Stores both the calculated CAGR value and
    its calculation status.

    value:
        CAGR percentage when calculation is valid.

    flag:
        Status or edge-case classification.
    """

    value: Optional[float]

    flag: str


# ==========================================================
# CAGR ENGINE
# ==========================================================

class CAGRCalculator:
    """
    Safe CAGR calculation engine.

    Formula:

    CAGR
    = (
        (Ending Value / Beginning Value)
        ** (1 / Number of Years)
        - 1
      ) × 100

    Supported flags:

    CALCULATED
    DECLINE_TO_LOSS
    TURNAROUND
    BOTH_NEGATIVE
    ZERO_BASE
    INSUFFICIENT
    INVALID_INPUT
    """

    # ------------------------------------------------------
    # Safe Numeric Conversion
    # ------------------------------------------------------

    @staticmethod
    def _to_float(value):

        if value is None:
            return None

        try:

            return float(value)

        except (
            TypeError,
            ValueError
        ):

            return None


    # ------------------------------------------------------
    # Core CAGR Formula
    # ------------------------------------------------------

    @staticmethod
    def calculate(
        start_value,
        end_value,
        years
    ) -> CAGRResult:
        """
        Calculate CAGR while handling financial-data
        edge cases.

        Edge-case rules:

        Positive → Positive
            Calculate CAGR normally.

        Positive → Negative
            DECLINE_TO_LOSS

        Negative → Positive
            TURNAROUND

        Negative → Negative
            BOTH_NEGATIVE

        Zero beginning value
            ZERO_BASE

        Missing or invalid values
            INVALID_INPUT

        Invalid period
            INSUFFICIENT
        """

        start_value = (
            CAGRCalculator
            ._to_float(
                start_value
            )
        )

        end_value = (
            CAGRCalculator
            ._to_float(
                end_value
            )
        )

        years = (
            CAGRCalculator
            ._to_float(
                years
            )
        )

        # --------------------------------------------------
        # Invalid or Missing Input
        # --------------------------------------------------

        if (
            start_value is None
            or end_value is None
            or years is None
        ):

            return CAGRResult(
                value=None,
                flag="INVALID_INPUT"
            )

        # --------------------------------------------------
        # Invalid Time Window
        # --------------------------------------------------

        if years <= 0:

            return CAGRResult(
                value=None,
                flag="INSUFFICIENT"
            )

        # --------------------------------------------------
        # Zero Base
        # --------------------------------------------------

        if start_value == 0:

            return CAGRResult(
                value=None,
                flag="ZERO_BASE"
            )

        # --------------------------------------------------
        # Positive to Negative
        # --------------------------------------------------

        if (
            start_value > 0
            and end_value < 0
        ):

            return CAGRResult(
                value=None,
                flag="DECLINE_TO_LOSS"
            )

        # --------------------------------------------------
        # Negative to Positive
        # --------------------------------------------------

        if (
            start_value < 0
            and end_value > 0
        ):

            return CAGRResult(
                value=None,
                flag="TURNAROUND"
            )

        # --------------------------------------------------
        # Negative to Negative
        # --------------------------------------------------

        if (
            start_value < 0
            and end_value < 0
        ):

            return CAGRResult(
                value=None,
                flag="BOTH_NEGATIVE"
            )

        # --------------------------------------------------
        # Positive to Zero
        # --------------------------------------------------

        if (
            start_value > 0
            and end_value == 0
        ):

            return CAGRResult(
                value=-100.0,
                flag="CALCULATED"
            )

        # --------------------------------------------------
        # Standard CAGR
        # --------------------------------------------------

        cagr = (
            (
                end_value
                / start_value
            )
            ** (
                1
                / years
            )
            - 1
        ) * 100

        return CAGRResult(
            value=round(
                cagr,
                4
            ),
            flag="CALCULATED"
        )


    # ------------------------------------------------------
    # CAGR from Historical Values
    # ------------------------------------------------------

    @staticmethod
    def calculate_from_history(
        values: Sequence,
        window: int
    ) -> CAGRResult:
        """
        Calculate CAGR from an ordered historical series.

        The values must be arranged from oldest
        to newest.

        Example:

        values = [
            100,
            120,
            140,
            160,
            180,
            200
        ]

        window = 5

        Beginning value = 100
        Ending value = 200
        Number of years = 5

        A five-year CAGR requires six annual observations:
        one beginning observation and five yearly intervals.
        """

        if values is None:

            return CAGRResult(
                value=None,
                flag="INSUFFICIENT"
            )

        values = list(values)

        required_observations = (
            window + 1
        )

        if (
            window <= 0
            or
            len(values)
            < required_observations
        ):

            return CAGRResult(
                value=None,
                flag="INSUFFICIENT"
            )

        selected_values = (
            values[
                -required_observations:
            ]
        )

        start_value = (
            selected_values[0]
        )

        end_value = (
            selected_values[-1]
        )

        return (
            CAGRCalculator
            .calculate(
                start_value=start_value,
                end_value=end_value,
                years=window
            )
        )


    # ------------------------------------------------------
    # Three-Year CAGR
    # ------------------------------------------------------

    @staticmethod
    def calculate_3yr(
        values
    ):

        return (
            CAGRCalculator
            .calculate_from_history(
                values=values,
                window=3
            )
        )


    # ------------------------------------------------------
    # Five-Year CAGR
    # ------------------------------------------------------

    @staticmethod
    def calculate_5yr(
        values
    ):

        return (
            CAGRCalculator
            .calculate_from_history(
                values=values,
                window=5
            )
        )


    # ------------------------------------------------------
    # Ten-Year CAGR
    # ------------------------------------------------------

    @staticmethod
    def calculate_10yr(
        values
    ):

        return (
            CAGRCalculator
            .calculate_from_history(
                values=values,
                window=10
            )
        )