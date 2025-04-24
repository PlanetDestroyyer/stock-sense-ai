from finvizfinance.screener.overview import Overview
import pandas as pd

def get_new_top_gainers():
    """Fetches top 10 gainers from Finviz."""
    try:
    
        screener = Overview()
        
        # Set filter for "Top Gainers" (stocks with highest % increase)
        screener.set_filter(filters_dict={'Change': 'Up 20%'})  # Adjust threshold as needed
        
        # Get data and sort by % change (descending)
        df = screener.screener_view()
        top_gainers = df.sort_values(by='Change', ascending=False).head(5)
        
        return top_gainers
    
    except Exception as e:
        print(f"❌ Error fetching gainers: {e}")
        return None

def get_top_losers():
    """Fetches top 10 losers from Finviz."""
    try:
        # Initialize screener
        screener = Overview()
        
        # Set filter for "Top Losers" (stocks with highest % decrease)
        screener.set_filter(filters_dict={'Change': 'Down 20%'})  # Adjust threshold as needed
        
        # Get data and sort by % change (ascending)
        df = screener.screener_view()
        top_losers = df.sort_values(by='Change', ascending=True).head(5)
        
        return top_losers
    
    except Exception as e:
        print(f"❌ Error fetching losers: {e}")
        return None

def format_movers(gainers, losers):
    """Formats the movers into readable strings."""
    if gainers is None or losers is None:
        return "❌ Failed to fetch data. Check Finviz connection."
    
    gainers_str = "📈 **Top 10 Gainers**\n" + gainers[['Ticker', 'Company', 'Change']].to_string(index=False)
    losers_str = "📉 **Top 10 Losers**\n" + losers[['Ticker', 'Company', 'Change']].to_string(index=False)
    
    return f"{gainers_str}\n\n{losers_str}"

# Example Usage
if __name__ == "__main__":
    gainers = get_new_top_gainers()
    losers = get_top_losers()
    print(gainers)
    print(losers)
    # print(format_movers(gainers, losers))