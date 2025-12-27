import yfinance as yf
import pandas as pd

def get_financials(ticker):
    """
    Pulls income statement, balance sheet, and cash flow statements.
    Returns a dictionary of DataFrames and stock info.
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Pull financials with error handling
        try:
            income_stmt = stock.financials.T  # Transpose for readability
        except:
            income_stmt = pd.DataFrame()
        
        try:
            balance_sheet = stock.balance_sheet.T
        except:
            balance_sheet = pd.DataFrame()
        
        try:
            cash_flow = stock.cashflow.T
        except:
            cash_flow = pd.DataFrame()
        
        # Convert index to string for Streamlit display
        if not income_stmt.empty:
            income_stmt.index = income_stmt.index.astype(str)
        if not balance_sheet.empty:
            balance_sheet.index = balance_sheet.index.astype(str)
        if not cash_flow.empty:
            cash_flow.index = cash_flow.index.astype(str)
        
        # Get stock info
        info = stock.info
        
        return {
            "Income Statement": income_stmt,
            "Balance Sheet": balance_sheet,
            "Cash Flow": cash_flow,
            "Info": info
        }
    except Exception as e:
        return {
            "Income Statement": pd.DataFrame(),
            "Balance Sheet": pd.DataFrame(),
            "Cash Flow": pd.DataFrame(),
            "Info": {"error": str(e)}
        }
