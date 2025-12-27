import yfinance as yf
import pandas as pd

def get_financials(ticker):
    """
    Pulls income statement, balance sheet, and cash flow statements.
    Returns a dictionary of DataFrames.
    """
    stock = yf.Ticker(ticker)
    
    # Pull financials
    income_stmt = stock.financials.T  # Transpose for readability
    balance_sheet = stock.balance_sheet.T
    cash_flow = stock.cashflow.T
    
    # Convert index to string for Streamlit display
    income_stmt.index = income_stmt.index.astype(str)
    balance_sheet.index = balance_sheet.index.astype(str)
    cash_flow.index = cash_flow.index.astype(str)
    
    return {
        "Income Statement": income_stmt,
        "Balance Sheet": balance_sheet,
        "Cash Flow": cash_flow
    }
