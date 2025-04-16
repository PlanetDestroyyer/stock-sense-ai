import pandas as pd
from finvizfinance.quote import finvizfinance



def stock_info(ticker):
    """
    Fetches stock information for a given ticker symbol.
    
    Args:
        ticker (str): The stock ticker symbol.
        
    Returns:
        dict: A dictionary containing stock information.
    """
    try:
        stock = finvizfinance(ticker)
        return stock.ticker_fundament()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
    return stock.ticker_fundament()

if __name__ == "__main__":
    pass
