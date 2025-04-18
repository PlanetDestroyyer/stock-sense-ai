from finvizfinance.quote import finvizfinance
from langchain.tools import tool
import pandas as pd
import logging


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


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def ticker_news(ticker: str) -> list:
    """Get news and latest price for the given ticker."""
    try:
        stock = finvizfinance(ticker)
        # Fetch fundamentals for price
        fundamentals = stock.ticker_fundament()
        logger.info(f"Fundamentals for {ticker}: {fundamentals}")
        price = fundamentals.get('Price', 'N/A')
        # Fetch news and convert DataFrame to list of dicts
        news_df = stock.ticker_news()
        logger.info(f"News DataFrame for {ticker}: {news_df.head()}")
        if isinstance(news_df, pd.DataFrame) and not news_df.empty:
            news = news_df.to_dict('records')  # Convert DataFrame to list of dictionaries
        else:
            news = []
        logger.info(f"Processed news for {ticker}: {news}")
        return [news, str(price)]  # Ensure price is a string
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    pass
