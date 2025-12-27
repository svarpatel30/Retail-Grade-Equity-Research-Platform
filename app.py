import streamlit as st

st.set_page_config(
    page_title="Retail Equity Research Platform",
    layout="wide"
)

st.title("📊 Retail Equity Research Platform")
st.caption("Transparent financial analysis and valuation")

ticker = st.text_input("Enter a stock ticker (e.g. AAPL)", value="AAPL")

st.divider()

st.header("Company Overview")
st.info("Company description will appear here.")

st.header("Financial Statements")
st.info("Income Statement, Balance Sheet, and Cash Flow will appear here.")

st.header("Key Metrics")
st.info("Financial ratios and performance metrics will appear here.")

st.header("Valuation (DCF)")
st.info("Intrinsic value and assumptions will appear here.")

st.header("Scenario Analysis")
st.info("Bull / Base / Bear case valuation ranges.")

st.divider()

st.header("Methodology")
st.write("""
This platform provides transparent, assumption-driven equity analysis.
Data is sourced from public financial statements and valuation logic
is intentionally simple and explainable.
""")
from data import get_financials
import streamlit as st

if ticker:
    financials = get_financials(ticker)
    
    for name, df in financials.items():
        st.subheader(name)
        st.dataframe(df)


