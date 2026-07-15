import pytest

from src.analytics.cagr import (
    CAGRCalculator
)


# ==========================================================
# STANDARD CAGR TESTS
# ==========================================================

def test_normal_cagr():

    result = (
        CAGRCalculator
        .calculate(
            start_value=100,
            end_value=200,
            years=5
        )
    )

    assert result.value == pytest.approx(
        14.8698,
        abs=0.0001
    )

    assert result.flag == "CALCULATED"


def test_declining_positive_cagr():

    result = (
        CAGRCalculator
        .calculate(
            start_value=200,
            end_value=100,
            years=5
        )
    )

    assert result.value == pytest.approx(
        -12.9449,
        abs=0.0001
    )

    assert result.flag == "CALCULATED"


# ==========================================================
# TURNAROUND TEST
# ==========================================================

def test_negative_to_positive_returns_turnaround():

    result = (
        CAGRCalculator
        .calculate(
            start_value=-100,
            end_value=200,
            years=5
        )
    )

    assert result.value is None

    assert result.flag == "TURNAROUND"


# ==========================================================
# DECLINE-TO-LOSS TEST
# ==========================================================

def test_positive_to_negative_returns_decline_to_loss():

    result = (
        CAGRCalculator
        .calculate(
            start_value=100,
            end_value=-50,
            years=5
        )
    )

    assert result.value is None

    assert (
        result.flag
        == "DECLINE_TO_LOSS"
    )


# ==========================================================
# BOTH-NEGATIVE TEST
# ==========================================================

def test_both_negative_returns_flag():

    result = (
        CAGRCalculator
        .calculate(
            start_value=-100,
            end_value=-50,
            years=5
        )
    )

    assert result.value is None

    assert (
        result.flag
        == "BOTH_NEGATIVE"
    )


# ==========================================================
# ZERO-BASE TEST
# ==========================================================

def test_zero_base_returns_flag():

    result = (
        CAGRCalculator
        .calculate(
            start_value=0,
            end_value=100,
            years=5
        )
    )

    assert result.value is None

    assert result.flag == "ZERO_BASE"


# ==========================================================
# INSUFFICIENT-HISTORY TESTS
# ==========================================================

def test_insufficient_history_returns_flag():

    result = (
        CAGRCalculator
        .calculate_from_history(
            values=[
                100,
                120,
                140
            ],
            window=5
        )
    )

    assert result.value is None

    assert (
        result.flag
        == "INSUFFICIENT"
    )


def test_invalid_year_window_returns_insufficient():

    result = (
        CAGRCalculator
        .calculate(
            start_value=100,
            end_value=200,
            years=0
        )
    )

    assert result.value is None

    assert (
        result.flag
        == "INSUFFICIENT"
    )


# ==========================================================
# MISSING-INPUT TEST
# ==========================================================

def test_missing_input_returns_invalid_input():

    result = (
        CAGRCalculator
        .calculate(
            start_value=None,
            end_value=200,
            years=5
        )
    )

    assert result.value is None

    assert (
        result.flag
        == "INVALID_INPUT"
    )


# ==========================================================
# POSITIVE-TO-ZERO TEST
# ==========================================================

def test_positive_to_zero_returns_negative_100_percent():

    result = (
        CAGRCalculator
        .calculate(
            start_value=100,
            end_value=0,
            years=5
        )
    )

    assert result.value == -100.0

    assert (
        result.flag
        == "CALCULATED"
    )


# ==========================================================
# WINDOW TESTS
# ==========================================================

def test_three_year_cagr():

    result = (
        CAGRCalculator
        .calculate_3yr(
            values=[
                100,
                120,
                150,
                200
            ]
        )
    )

    assert result.value == pytest.approx(
        25.9921,
        abs=0.0001
    )

    assert (
        result.flag
        == "CALCULATED"
    )


def test_five_year_cagr():

    result = (
        CAGRCalculator
        .calculate_5yr(
            values=[
                100,
                110,
                125,
                145,
                170,
                200
            ]
        )
    )

    assert result.value == pytest.approx(
        14.8698,
        abs=0.0001
    )

    assert (
        result.flag
        == "CALCULATED"
    )


def test_ten_year_cagr():

    result = (
        CAGRCalculator
        .calculate_10yr(
            values=[
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200
            ]
        )
    )

    assert result.value == pytest.approx(
        7.1773,
        abs=0.0001
    )

    assert (
        result.flag
        == "CALCULATED"
    )