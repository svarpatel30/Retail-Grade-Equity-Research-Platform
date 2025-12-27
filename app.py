import streamlit as st
from data import get_financials
from metrics import calculate_key_metrics

# Page setup
st.set_page_config(
    page_title="Retail Equity Research Platform",
    layout="wide"
)

st.title("📊 Retail Equity Research Platform")
st.caption("Transparent financial analysis and valuation")

ticker = st.text_input("Enter a stock ticker (e.g. AAPL)", value="AAPL")

st.divider()

# Company Overview
st.header("Company Overview")
st.info("Company description will appear here.")

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
st.info("Intrinsic value and assumptions will appear here.")

# Scenario Analysis
st.header("Scenario Analysis")
st.info("Bull / Base / Bear case valuation ranges.")

st.divider()

# Methodology
st.header("Methodology")
st.write("""
This platform provides transparent, assumption-driven equity analysis.
Data is sourced from public financial statements and valuation logic
is intentionally simple and explainable.
""")
