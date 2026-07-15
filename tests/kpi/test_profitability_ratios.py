import pytest

from src.analytics.ratios import (
    FinancialRatioCalculator
)


# ==========================================================
# NET PROFIT MARGIN TESTS
# ==========================================================

def test_net_profit_margin_normal_case():

    result = (
        FinancialRatioCalculator
        .net_profit_margin(
            net_profit=200,
            sales=1000
        )
    )

    assert result == 20.0


def test_net_profit_margin_zero_sales_returns_none():

    result = (
        FinancialRatioCalculator
        .net_profit_margin(
            net_profit=200,
            sales=0
        )
    )

    assert result is None


# ==========================================================
# OPERATING PROFIT MARGIN TESTS
# ==========================================================

def test_operating_profit_margin_normal_case():

    result = (
        FinancialRatioCalculator
        .operating_profit_margin(
            operating_profit=250,
            sales=1000
        )
    )

    assert result == 25.0


def test_operating_profit_margin_zero_sales_returns_none():

    result = (
        FinancialRatioCalculator
        .operating_profit_margin(
            operating_profit=250,
            sales=0
        )
    )

    assert result is None


def test_opm_cross_check_detects_mismatch():

    result = (
        FinancialRatioCalculator
        .cross_check_operating_margin(
            operating_profit=250,
            sales=1000,
            source_opm_percentage=20
        )
    )

    assert result.value == 25.0

    assert result.source_value == 20.0

    assert result.difference == 5.0

    assert result.flag == "OPM_MISMATCH"


def test_opm_cross_check_accepts_matching_value():

    result = (
        FinancialRatioCalculator
        .cross_check_operating_margin(
            operating_profit=250,
            sales=1000,
            source_opm_percentage=24.5
        )
    )

    assert result.value == 25.0

    assert result.difference == 0.5

    assert result.flag == "MATCH"


# ==========================================================
# RETURN ON EQUITY TESTS
# ==========================================================

def test_return_on_equity_normal_case():

    result = (
        FinancialRatioCalculator
        .return_on_equity(
            net_profit=150,
            equity_capital=250,
            reserves=750
        )
    )

    assert result == 15.0


def test_return_on_equity_negative_equity_returns_none():

    result = (
        FinancialRatioCalculator
        .return_on_equity(
            net_profit=150,
            equity_capital=100,
            reserves=-200
        )
    )

    assert result is None


# ==========================================================
# ADDITIONAL PROFITABILITY TESTS
# ==========================================================

def test_return_on_capital_employed():

    result = (
        FinancialRatioCalculator
        .return_on_capital_employed(
            ebit=200,
            equity_capital=200,
            reserves=500,
            borrowings=300
        )
    )

    assert result == 20.0


def test_return_on_assets():

    result = (
        FinancialRatioCalculator
        .return_on_assets(
            net_profit=100,
            total_assets=2000
        )
    )

    assert result == 5.0


def test_financial_sector_uses_relative_roce_benchmark():

    result = (
        FinancialRatioCalculator
        .get_roce_benchmark_type(
            broad_sector="Financials"
        )
    )

    assert result == "SECTOR_RELATIVE"


def test_nonfinancial_sector_uses_absolute_roce_benchmark():

    result = (
        FinancialRatioCalculator
        .get_roce_benchmark_type(
            broad_sector="Information Technology"
        )
    )

    assert result == "ABSOLUTE"