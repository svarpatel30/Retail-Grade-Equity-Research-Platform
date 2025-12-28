import pandas as pd
import numpy as np

def run_dcf_model(financials, assumptions):
    """
    Discounted Cash Flow valuation model (updated for realistic results for large companies)
    """
    try:
        income_stmt = financials["Income Statement"]
        balance_sheet = financials["Balance Sheet"]
        cash_flow = financials["Cash Flow"]
        info = financials["Info"]
        market_cap = info.get("marketCap", 0)

        # Assumptions (define first!)
        discount_rate = assumptions.get("discount_rate", 0.10)
        terminal_growth = assumptions.get("terminal_growth", 0.025)
        projection_years = assumptions.get("projection_years", 5)
        revenue_growth = assumptions.get("revenue_growth", 0.05)
        margin_improvement = assumptions.get("margin_improvement", 0.005)

        # Adjust for mega-cap companies
        if market_cap > 1_000_000_000_000:
            discount_rate = max(discount_rate, 0.075)  # slightly lower WACC
            terminal_growth = max(terminal_growth, 0.03)  # more realistic long-term growth

        # Historical FCF
        historical_fcf = calculate_historical_fcf(cash_flow)
        if historical_fcf.empty:
            return {"Error": "Unable to calculate historical free cash flow"}

        # Latest financials
        latest_income = income_stmt.iloc[0]
        latest_balance = balance_sheet.iloc[0]

        revenue = latest_income.get("Total Revenue", 0)
        operating_income = latest_income.get("Operating Income", 0)
        operating_margin = operating_income / revenue if revenue else 0

        # Project FCF
        projected_cf = project_cash_flows(
            last_fcf=historical_fcf.iloc[-1],
            revenue=revenue,
            margin=operating_margin,
            revenue_growth=revenue_growth,
            margin_improvement=margin_improvement,
            years=projection_years,
            company_size=market_cap
        )

        terminal_value = projected_cf[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)

        discounted_cf = [
            cf / ((1 + discount_rate) ** (i + 1))
            for i, cf in enumerate(projected_cf)
        ]

        pv_terminal = terminal_value / ((1 + discount_rate) ** projection_years)
        enterprise_value = sum(discounted_cf) + pv_terminal

        cash = latest_balance.get("Cash And Cash Equivalents", 0)
        debt = (
            latest_balance.get("Short Long Term Debt", 0) +
            latest_balance.get("Long Term Debt", 0)
        )

        equity_value = enterprise_value - debt + cash

        shares_outstanding = info.get("sharesOutstanding", 0)
        value_per_share = equity_value / shares_outstanding if shares_outstanding else 0
        current_price = info.get("currentPrice", 0)

        return {
            "Enterprise Value": enterprise_value,
            "Equity Value": equity_value,
            "Value per Share": value_per_share,
            "Current Price": current_price,
            "Upside/Downside": ((value_per_share - current_price) / current_price) if current_price else 0,
            "Projected FCF": projected_cf,
            "Terminal Value": terminal_value,
            "Assumptions": {
                "Discount Rate": f"{discount_rate:.1%}",
                "Terminal Growth": f"{terminal_growth:.1%}",
                "Revenue Growth": f"{revenue_growth:.1%}",
                "Margin Improvement": f"{margin_improvement:.1%}",
                "Projection Years": projection_years
            }
        }

    except Exception as e:
        return {"Error": str(e)}

def calculate_historical_fcf(cash_flow):
    """
    FCF = Operating Cash Flow - CapEx
    """
    fcf = []
    for _, row in cash_flow.iterrows():
        ocf = row.get("Operating Cash Flow", 0)
        capex = (
            row.get("Capital Expenditure", 0) or
            row.get("Capital Expenditures", 0) or
            row.get("Purchase Of PPE", 0) or
            row.get("Capital expenditures", 0)
        )
        fcf.append(ocf - abs(capex))
    return pd.Series(fcf)

def project_cash_flows(last_fcf, revenue, margin, revenue_growth, margin_improvement, years, company_size):
    """
    Project future free cash flows realistically
    """
    projected = []
    current_margin = margin

    # Adjust FCF conversion ratio for mega-cap companies
    fcf_conversion = 0.85 if company_size > 1_000_000_000_000 else 0.80

    for year in range(years):
        revenue *= (1 + revenue_growth)
        current_margin = min(current_margin + margin_improvement, 0.35)  # allow margin improvement up to 35%
        operating_income = revenue * current_margin
        fcf = operating_income * fcf_conversion

        # Ensure FCF is not too low compared to historical
        if year == 0:
            fcf = max(fcf, last_fcf * (1 + revenue_growth * 0.5))

        projected.append(fcf)

    return projected
