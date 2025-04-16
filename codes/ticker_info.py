import pandas as pd
from finvizfinance.quote import finvizfinance
from langchain.tools import tool


@tool
def stock_info(ticker: str) -> str:
    """Get stock info for the given ticker."""
    ...

    try:
        stock = finvizfinance(ticker)
        return stock.ticker_fundament()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
    return stock.ticker_fundament()

@tool
def ticker_news(ticker: str) -> str:
    """Get news for the given ticker."""
    try:
        stock = finvizfinance(ticker)
        return stock.ticker_news()
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
    return stock.ticker_news()


if __name__ == "__main__":
    pass
