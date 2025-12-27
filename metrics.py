import pandas as pd

def calculate_key_metrics(financials):
    """
    Compute key financial ratios.
    """
    income_stmt = financials["Income Statement"]
    balance_sheet = financials["Balance Sheet"]
    cash_flow = financials["Cash Flow"]
    info = financials["Info"]
    
    # Get latest data (first row)
    latest_income = income_stmt.iloc[0]
    latest_balance = balance_sheet.iloc[0]
    
    # Get previous year data if available
    if len(income_stmt) > 1:
        previous_income = income_stmt.iloc[1]
        previous_balance = balance_sheet.iloc[1]
    else:
        previous_income = None
        previous_balance = None
    
    # Extract values
    try:
        total_revenue = latest_income.get('Total Revenue', latest_income.get('Revenue', 0))
        gross_profit = latest_income.get('Gross Profit', 0)
        operating_income = latest_income.get('Operating Income', 0)
        net_income = latest_income.get('Net Income', 0)
        
        total_assets = latest_balance.get('Total Assets', 0)
        current_assets = latest_balance.get('Current Assets', 0)
        current_liabilities = latest_balance.get('Current Liabilities', 0)
        inventory = latest_balance.get('Inventory', 0)

        short_term_debt = latest_balance.get('Short Long Term Debt', 0)
        long_term_debt = latest_balance.get('Long Term Debt', 0)
        total_debt = short_term_debt + long_term_debt
        
        total_equity = latest_balance.get('Total Equity Gross Minority Interest', 0) 
        current_price = info.get('currentPrice', 0)
        shares_outstanding = info.get('sharesOutstanding', 0)
        
        # Compute ratios
        ratios = {}
        
        # Profitability Ratios
        if total_revenue != 0:
            ratios['Gross Margin'] = gross_profit / total_revenue
            ratios['Operating Margin'] = operating_income / total_revenue
            ratios['Net Margin'] = net_income / total_revenue
        
        # Liquidity Ratios
        if current_liabilities != 0:
            ratios['Current Ratio'] = current_assets / current_liabilities
            ratios['Quick Ratio'] = (current_assets - inventory) / current_liabilities
        
        # Leverage Ratios
        if total_equity != 0:
            avg_equity = balance_sheet.iloc[:2]['Total Equity Gross Minority Interest'].mean()
            avg_assets = balance_sheet.iloc[:2]['Total Assets'].mean()
            ROE = net_income / avg_equity
            ROA = net_income / avg_assets
        
        # Efficiency Ratios
        if total_assets != 0:
            ratios['Return on Assets (ROA)'] = net_income / total_assets
        
        # Valuation Ratios
        if shares_outstanding != 0:
            eps = net_income / shares_outstanding
            book_value_per_share = total_equity / shares_outstanding
            if eps != 0:
                ratios['P/E Ratio'] = current_price / eps
            if book_value_per_share != 0:
                ratios['P/B Ratio'] = current_price / book_value_per_share
        
        # YoY Growth Metrics
        if previous_income is not None and previous_balance is not None:
            prev_revenue = previous_income.get('Total Revenue', previous_income.get('Revenue', 0))
            prev_net_income = previous_income.get('Net Income', 0)
            prev_total_assets = previous_balance.get('Total Assets', 0)
            prev_total_equity = previous_balance.get('Total Equity Gross Minority Interest', 0)
            
            if prev_revenue != 0:
                ratios['YoY Revenue Growth'] = (total_revenue - prev_revenue) / prev_revenue
            if prev_net_income != 0:
                ratios['YoY Net Income Growth'] = (net_income - prev_net_income) / prev_net_income
            if prev_total_assets != 0:
                ratios['YoY Assets Growth'] = (total_assets - prev_total_assets) / prev_total_assets
            if prev_total_equity != 0:
                ratios['YoY Equity Growth'] = (total_equity - prev_total_equity) / prev_total_equity
            
            # EPS Growth
            prev_eps = prev_net_income / shares_outstanding if shares_outstanding != 0 else 0
            if prev_eps != 0:
                ratios['YoY EPS Growth'] = (eps - prev_eps) / prev_eps
        
        # Format as percentages where appropriate
        formatted_ratios = {}
        for key, value in ratios.items():
            if 'Margin' in key or 'Return' in key or 'Growth' in key:
                formatted_ratios[key] = f"{value:.2%}"
            elif 'Ratio' in key:
                formatted_ratios[key] = f"{value:.2f}"
            else:
                formatted_ratios[key] = f"{value:.2f}"
        
        return formatted_ratios
    except Exception as e:
        return {"Error": str(e)}

