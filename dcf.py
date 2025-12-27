import pandas as pd
import numpy as np

# ---------------------------------------------------------
# MAIN DCF RUNNER
# ---------------------------------------------------------

def run_dcf_model(financials, assumptions=None):
    """
    Discounted Cash Flow valuation with scenario analysis.

    Args:
        financials: Dictionary containing financial statements
        assumptions: Optional dictionary of base-case assumptions

    Returns:
        Dictionary with Bull / Base / Bear valuation outputs
    """

    if assumptions is None:
        assumptions = {}

    try:
        income_stmt = financials["Income Statement"]
        balance_sheet = financials["Balance Sheet"]
        cash_flow = financials["Cash Flow"]
        info = financials["Info"]

        # -------------------------------
        # Base assumptions (editable)
        # -------------------------------
        base_discount_rate = assumptions.get("discount_rate", 0.10)
        base_terminal_growth = assumptions.get("terminal_growth", 0.025)
        base_revenue_growth = assumptions.get("revenue_growth", 0.05)
        margin_improvement = assumptions.get("margin_improvement", 0.005)
        projection_years = assumptions.get("projection_years", 5)

        # -------------------------------
        # Scenario definitions
        # -------------------------------
        scenarios = {
            "Bull": {
                "discount_rate": base_discount_rate - 0.01,
                "revenue_growth": base_revenue_growth + 0.02
            },
            "Base": {
                "discount_rate": base_discount_rate,
                "revenue_growth": base_revenue_growth
            },
            "Bear": {
                "discount_rate": base_discount_rate + 0.01,
                "revenue_growth": base_revenue_growth - 0.02
            }
        }

        # -------------------------------
        # Historical Free Cash Flow
        # -------------------------------
        historical_fcf = calculate_historical_fcf(cash_flow)

        if historical_fcf.empty:
            return {"Error": "Unable to calculate historical free cash flow"}

        # Ensure correct chronological order
        last_fcf = historical_fcf.sort_index().iloc[-1]

        # -------------------------------
        # Latest financials
        # -------------------------------
        latest_income = income_stmt.iloc[0]
        latest_balance = balance_sheet.iloc[0]

        total_revenue = latest_income.get("Total Revenue", latest_income.get("Revenue", 0))
        operating_income = latest_income.get("Operating Income", 0)

        operating_margin = (
            operating_income / total_revenue if total_revenue != 0 else 0
        )

        # Balance sheet items
        cash_and_equivalents = latest_balance.get("Cash And Cash Equivalents", 0)
        total_debt = (
            latest_balance.get("Short Long Term Debt", 0)
            + latest_balance.get("Long Term Debt", 0)
        )
        minority_interest = latest_balance.get("Minority Interest", 0)

        shares_outstanding = info.get("sharesOutstanding", 0)
        current_price = info.get("currentPrice", 0)

        # -------------------------------
        # Run scenarios
        # -------------------------------
        results = {}

        for name, params in scenarios.items():
            valuation = run_single_dcf(
                last_fcf=last_fcf,
                revenue=total_revenue,
                margin=operating_margin,
                revenue_growth=params["revenue_growth"],
                margin_improvement=margin_improvement,
                discount_rate=params["discount_rate"],
                terminal_growth=base_terminal_growth,
                years=projection_years,
                cash=cash_and_equivalents,
                debt=total_debt,
                minority_interest=minority_interest,
                shares_outstanding=shares_outstanding,
                current_price=current_price
            )

            results[name] = valuation

        return {
            "Valuation Summary": results,
            "Assumptions": {
                "Terminal Growth": f"{base_terminal_growth:.1%}",
                "Margin Improvement": f"{margin_improvement:.1%}",
                "Projection Years": projection_years
            }
        }

    except Exception as e:
        return {"Error": str(e)}


# ---------------------------------------------------------
# SINGLE DCF CALCULATION
# ---------------------------------------------------------

def run_single_dcf(
    last_fcf,
    revenue,
    margin,
    revenue_growth,
    margin_improvement,
    discount_rate,
    terminal_growth,
    years,
    cash,
    debt,
    minority_interest,
    shares_outstanding,
    current_price
):
    """
    Runs one DCF scenario.
    """

    projected_cf = project_cash_flows(
        last_fcf,
        revenue,
        margin,
        revenue_growth,
        margin_improvement,
        years
    )

    # Terminal value (Gordon Growth)
    terminal_value = projected_cf[-1] * (1 + terminal_growth) / (
        discount_rate - terminal_growth
    )

    # Discount cash flows
    discounted_cf = [
        cf / ((1 + discount_rate) ** (i + 1))
        for i, cf in enumerate(projected_cf)
    ]

    pv_terminal = terminal_value / ((1 + discount_rate) ** years)

    enterprise_value = sum(discounted_cf) + pv_terminal

    equity_value = enterprise_value - debt + cash - minority_interest

    value_per_share = (
        equity_value / shares_outstanding if shares_outstanding > 0 else 0
    )

    upside = (
        (value_per_share - current_price) / current_price
        if current_price != 0 else 0
    )

    return {
        "Enterprise Value": enterprise_value,
        "Equity Value": equity_value,
        "Value per Share": value_per_share,
        "Current Price": current_price,
        "Upside / Downside": upside
    }


# ---------------------------------------------------------
# FREE CASH FLOW CALCULATION
# ---------------------------------------------------------

def calculate_historical_fcf(cash_flow):
    """
    FCF = Operating Cash Flow - Capital Expenditures
    """

    fcf_values = []

    for _, row in cash_flow.iterrows():
        ocf = row.get("Operating Cash Flow", 0)

        capex = (
            row.get("Capital Expenditure", 0)
            or row.get("Capital Expenditures", 0)
            or -row.get("Additions to property, plant and equipment", 0)
        )

        if capex == 0:
            depreciation = row.get("Depreciation", 0)
            capex = depreciation  # maintenance CapEx assumption

        fcf = ocf - capex
        fcf_values.append(fcf)

    return pd.Series(fcf_values, index=cash_flow.index[:len(fcf_values)])


# ---------------------------------------------------------
# CASH FLOW PROJECTIONS
# ---------------------------------------------------------

def project_cash_flows(
    last_fcf,
    revenue,
    margin,
    revenue_growth,
    margin_improvement,
    years
):
    """
    Projects future free cash flows using revenue growth
    and margin expansion assumptions.
    """

    projected_cf = []
    current_revenue = revenue
    current_margin = margin

    for year in range(years):
        current_revenue *= (1 + revenue_growth)
        current_margin = min(current_margin + margin_improvement, 0.30)

        operating_income = current_revenue * current_margin

        # Simplified FCF conversion assumption
        fcf_conversion = 0.8
        projected_fcf = operating_income * fcf_conversion

        if year == 0:
            projected_fcf = max(
                projected_fcf,
                last_fcf * (1 + revenue_growth * 0.5)
            )

        projected_cf.append(projected_fcf)

    return projected_cf
