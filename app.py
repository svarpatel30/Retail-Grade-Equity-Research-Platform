import streamlit as st
import pandas as pd
from data import get_financials
from metrics import calculate_key_metrics
from dcf import run_dcf_model, calculate_dcf

# Page setup
st.set_page_config(
    page_title="Retail Equity Research Platform",
    layout="wide"
)

st.title("📊 Retail Equity Research Platform")
st.caption("Transparent financial analysis and valuation")

ticker = st.text_input("Enter a stock ticker (e.g. AAPL)", value="AAPL")

st.divider()

if ticker:
    # ✅ Always fetch financials first
    financials = get_financials(ticker)
# Company Overview
st.header("Company Overview")

info = financials["Info"]

st.subheader(info.get("shortName", ticker))
st.caption(info.get("industry", "N/A"))

col1, col2, col3 = st.columns(3)

col1.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B")
col2.metric("Revenue", f"${info.get('totalRevenue', 0)/1e9:.1f}B")
col3.metric("Net Income", f"${info.get('netIncomeToCommon', 0)/1e9:.1f}B")

st.write(info.get("longBusinessSummary", ""))


# Financial Statements
st.header("Financial Statements")
if ticker:
    financials = get_financials(ticker)
    for name, df in financials.items():
        if name == "Info":
            continue
        st.subheader(name)
        # Divide all numbers by 1 million for readability
        df_m = df / 1_000_000
        st.dataframe(df_m.style.format("${:,.0f}M"))

# Key Metrics
st.header("Key Metrics")
if ticker:
    metrics = calculate_key_metrics(financials)
    if metrics and "Error" not in metrics:
        # Descriptions for each metric
        descriptions = {
            'Gross Margin': 'Profit after cost of goods sold as % of revenue',
            'Operating Margin': 'Operating profit as % of revenue',
            'Net Margin': 'Net profit as % of revenue',
            'Current Ratio': 'Ability to pay short-term obligations',
            'Quick Ratio': 'Ability to pay short-term obligations without inventory',
            'Debt-to-Equity': 'Financial leverage ratio',
            'Return on Equity (ROE)': 'Profitability relative to shareholders\' equity',
            'Return on Assets (ROA)': 'Profitability relative to total assets',
            'P/E Ratio': 'Price per share relative to earnings per share',
            'P/B Ratio': 'Price per share relative to book value per share',
            'YoY Revenue Growth': 'Year-over-year change in total revenue',
            'YoY Net Income Growth': 'Year-over-year change in net income',
            'YoY Assets Growth': 'Year-over-year change in total assets',
            'YoY Equity Growth': 'Year-over-year change in shareholders\' equity',
            'YoY EPS Growth': 'Year-over-year change in earnings per share'
        }
        
        # Group metrics by category
        profitability_ratios = ['Gross Margin', 'Operating Margin', 'Net Margin']
        liquidity_ratios = ['Current Ratio', 'Quick Ratio']
        leverage_ratios = ['Debt-to-Equity', 'Return on Equity (ROE)']
        efficiency_ratios = ['Return on Assets (ROA)']
        valuation_ratios = ['P/E Ratio', 'P/B Ratio']
        growth_ratios = ['YoY Revenue Growth', 'YoY Net Income Growth', 'YoY EPS Growth', 'YoY Assets Growth', 'YoY Equity Growth']
        
        # Display each group
        groups = [
            ("Profitability Ratios", profitability_ratios),
            ("Liquidity Ratios", liquidity_ratios),
            ("Leverage Ratios", leverage_ratios),
            ("Efficiency Ratios", efficiency_ratios),
            ("Valuation Ratios", valuation_ratios),
            ("Growth Metrics", growth_ratios)
        ]
        
        for group_name, ratio_list in groups:
            st.subheader(group_name)
            cols = st.columns(len(ratio_list))
            for i, ratio in enumerate(ratio_list):
                if ratio in metrics:
                    cols[i].metric(ratio, metrics[ratio])
                    cols[i].caption(descriptions.get(ratio, ""))
    else:
        st.info("Unable to calculate metrics.")
else:
    st.info("Financial ratios and performance metrics will appear here.")

# Valuation (DCF)
st.header("Valuation (DCF)")

if ticker:
    # DCF Assumptions
    st.subheader("DCF Assumptions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        discount_rate = st.slider("Discount Rate (WACC)", 0.05, 0.20, 0.10, 0.01, help="Required rate of return")
        terminal_growth = st.slider("Terminal Growth Rate", 0.00, 0.05, 0.025, 0.005, help="Long-term growth rate")
    
    with col2:
        revenue_growth = st.slider("Revenue Growth Rate", -0.10, 0.20, 0.05, 0.01, help="Annual revenue growth")
        margin_improvement = st.slider("Margin Improvement", -0.02, 0.02, 0.005, 0.001, help="Annual operating margin improvement")
    
    with col3:
        projection_years = st.slider("Projection Years", 3, 10, 5, 1, help="Number of years to project cash flows")
    
    assumptions = {
        'discount_rate': discount_rate,
        'terminal_growth': terminal_growth,
        'projection_years': projection_years,
        'revenue_growth': revenue_growth,
        'margin_improvement': margin_improvement
    }
    
    # Run DCF
    dcf_result = run_dcf_model(financials, assumptions)
    
    if "Error" not in dcf_result:
        st.subheader("DCF Valuation Results")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Intrinsic Value per Share", f"${dcf_result['Value per Share']:.2f}")
        with col2:
            st.metric("Current Price", f"${dcf_result['Current Price']:.2f}")
        with col3:
            upside = dcf_result['Upside/Downside']
            st.metric("Upside/Downside", f"{upside:.1%}", 
                     delta=f"{upside:.1%}" if upside > 0 else f"{upside:.1%}",
                     delta_color="normal" if upside > 0 else "inverse")
        with col4:
            st.metric("Enterprise Value", f"${dcf_result['Enterprise Value']/1e9:.1f}B")
        
        # Assumptions summary
        st.subheader("Assumptions Used")
        assumptions = dcf_result['Assumptions']
        col1, col2, col3 = st.columns(3)
        for i, (key, value) in enumerate(assumptions.items()):
            if i % 3 == 0:
                col1.metric(key, value)
            elif i % 3 == 1:
                col2.metric(key, value)
            else:
                col3.metric(key, value)
        
        # Projected Cash Flows
        st.subheader("Projected Free Cash Flows")
        years = [f"Year {i+1}" for i in range(projection_years)]
        projected_df = pd.DataFrame({
            'Year': years,
            'Projected FCF': dcf_result['Projected FCF']
        })
        projected_df['Projected FCF'] = projected_df['Projected FCF'].apply(lambda x: f"${x/1e6:.0f}M")
        st.dataframe(projected_df)
        
        st.caption(f"Terminal Value: ${dcf_result['Terminal Value']/1e9:.1f}B")
    else:
        st.error(f"DCF calculation failed: {dcf_result['Error']}")
else:
    st.info("Enter a ticker symbol to see DCF valuation.")

# Scenario Analysis
st.header("Scenario Analysis")

scenarios = {
    "Bear": {
        "discount_rate": 0.10,
        "terminal_growth": 0.02,
        "revenue_growth": 0.03,
        "margin_improvement": 0.002
    },
    "Base": {
        "discount_rate": 0.075,
        "terminal_growth": 0.03,
        "revenue_growth": 0.05,
        "margin_improvement": 0.005
    },
    "Bull": {
        "discount_rate": 0.065,
        "terminal_growth": 0.035,
        "revenue_growth": 0.07,
        "margin_improvement": 0.008
    }
}

cols = st.columns(3)

for col, (name, params) in zip(cols, scenarios.items()):
    with col:
        scenario_assumptions = {
            "discount_rate": params["discount_rate"],
            "terminal_growth": params["terminal_growth"],
            "revenue_growth": params["revenue_growth"],
            "margin_improvement": params["margin_improvement"],
            "projection_years": projection_years
        }

        dcf = run_dcf_model(financials, scenario_assumptions)

        st.subheader(name)

        if "Error" not in dcf:
            st.metric(
                "Intrinsic Value per Share",
                f"${dcf['Value per Share']:.2f}"
            )
        else:
            st.error("DCF failed")

st.divider()

# Methodology
st.header("Methodology")
st.write("""
This platform provides transparent, assumption-driven equity analysis.
Data is sourced from public financial statements and valuation logic
is intentionally simple and explainable.
""")