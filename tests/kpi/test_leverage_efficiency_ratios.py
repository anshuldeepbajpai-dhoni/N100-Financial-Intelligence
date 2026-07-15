from src.analytics.ratios import (
    FinancialRatioCalculator
)


# ==========================================================
# DEBT-TO-EQUITY TESTS
# ==========================================================

def test_debt_to_equity_normal_case():

    result = (
        FinancialRatioCalculator
        .debt_to_equity(
            borrowings=500,
            equity_capital=200,
            reserves=800
        )
    )

    assert result == 0.5


def test_debt_free_company_returns_zero_debt_to_equity():

    result = (
        FinancialRatioCalculator
        .debt_to_equity(
            borrowings=0,
            equity_capital=200,
            reserves=800
        )
    )

    assert result == 0.0


def test_debt_to_equity_negative_equity_returns_none():

    result = (
        FinancialRatioCalculator
        .debt_to_equity(
            borrowings=500,
            equity_capital=100,
            reserves=-200
        )
    )

    assert result is None


# ==========================================================
# HIGH-LEVERAGE TESTS
# ==========================================================

def test_high_debt_to_equity_flags_nonfinancial_company():

    result = (
        FinancialRatioCalculator
        .high_leverage_flag(
            debt_to_equity=6.5,
            broad_sector="Industrials"
        )
    )

    assert result is True


def test_financial_sector_suppresses_high_leverage_flag():

    result = (
        FinancialRatioCalculator
        .high_leverage_flag(
            debt_to_equity=8.0,
            broad_sector="Financials"
        )
    )

    assert result is False


# ==========================================================
# INTEREST-COVERAGE TESTS
# ==========================================================

def test_interest_coverage_normal_case():

    result = (
        FinancialRatioCalculator
        .interest_coverage_ratio(
            operating_profit=400,
            other_income=100,
            interest=100
        )
    )

    assert result == 5.0


def test_interest_coverage_zero_interest_returns_none():

    result = (
        FinancialRatioCalculator
        .interest_coverage_ratio(
            operating_profit=400,
            other_income=100,
            interest=0
        )
    )

    assert result is None


def test_zero_interest_receives_debt_free_label():

    ratio = (
        FinancialRatioCalculator
        .interest_coverage_ratio(
            operating_profit=400,
            other_income=100,
            interest=0
        )
    )

    label = (
        FinancialRatioCalculator
        .interest_coverage_label(
            interest_coverage=ratio,
            interest=0
        )
    )

    assert label == "Debt Free"


def test_low_interest_coverage_receives_warning():

    result = (
        FinancialRatioCalculator
        .interest_coverage_warning(
            interest_coverage=1.2
        )
    )

    assert result is True


def test_healthy_interest_coverage_has_no_warning():

    result = (
        FinancialRatioCalculator
        .interest_coverage_warning(
            interest_coverage=3.5
        )
    )

    assert result is False


# ==========================================================
# NET-DEBT TESTS
# ==========================================================

def test_net_debt():

    result = (
        FinancialRatioCalculator
        .net_debt(
            borrowings=1000,
            investments=400
        )
    )

    assert result == 600.0


def test_negative_net_debt_is_preserved():

    result = (
        FinancialRatioCalculator
        .net_debt(
            borrowings=300,
            investments=500
        )
    )

    assert result == -200.0


# ==========================================================
# ASSET-TURNOVER TESTS
# ==========================================================

def test_asset_turnover():

    result = (
        FinancialRatioCalculator
        .asset_turnover(
            sales=2000,
            total_assets=1000
        )
    )

    assert result == 2.0


def test_asset_turnover_zero_assets_returns_none():

    result = (
        FinancialRatioCalculator
        .asset_turnover(
            sales=2000,
            total_assets=0
        )
    )

    assert result is None