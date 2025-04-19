from finvizfinance.quote import finvizfinance
import pandas as pd

def compare_stocks(ticker1: str, ticker2: str) -> str:
    """
    Compare key fundamentals of two stocks using their tickers.
    Returns a side-by-side comparison table as a string.
    """
    try:
        stock1 = finvizfinance(ticker1)
        stock2 = finvizfinance(ticker2)

        fundamentals1 = stock1.ticker_fundament()
        fundamentals2 = stock2.ticker_fundament()

        keys_to_compare = [
    'Price', 'P/E', 'Forward P/E', 'PEG', 'EPS (ttm)', 'EPS next 5Y',
    'Dividend %', 'ROA', 'ROE', 'Gross Margin', 'Operating Margin',
    'Profit Margin', 'Current Ratio', 'Debt/Eq',
    'Market Cap', 'Beta', 'ATR', 'RSI (14)', 'SMA50', 'SMA200',
    '52W High', '52W Low', 'Insider Own', 'Insider Trans', 'Inst Own'
]


        data = {
            f"{ticker1.upper()}": [fundamentals1.get(k, 'N/A') for k in keys_to_compare],
            f"{ticker2.upper()}": [fundamentals2.get(k, 'N/A') for k in keys_to_compare]
        }

        df = pd.DataFrame(data, index=keys_to_compare)
        return df.to_string()
    
    except Exception as e:
        return f"❌ Error comparing stocks: {e}"

if __name__ == "__main__":
    print("📊 Stock Comparison Tool")
    ticker1 = input("Enter first stock ticker (e.g. AAPL): ").upper()
    ticker2 = input("Enter second stock ticker (e.g. MSFT): ").upper()
    
    result = compare_stocks(ticker1, ticker2)
    print("\n📝 Comparison Result:\n")
    print(result)
