from finvizfinance.screener.overview import Overview
import pandas as pd

def get_top_gainers():
    """
    Fetches top gainers from Finviz using finvizfinance package.
    
    Returns:
        str: Formatted string containing top gainers data
    """
    # Create a screener object
    foverview = Overview()
    
    # Use "Change" filter for top gainers (stocks with highest positive change)
    filters_dict = {'Change': 'Top Gainers'}  # This will filter for stocks with high positive change
    foverview.set_filter(filters_dict=filters_dict)
    
    # Get the data
    df = foverview.screener_view()
    
    # Sort by Change (%) in descending order
    df = df.sort_values(by='Change', ascending=False)
    
    # Select top 10 records
    top_gainers = df.head(10)
    
    # Format as string
    result = "Top Gainers:\n"
    result += top_gainers.to_string(index=False)
    
    return result

def get_top_losers():
    """
    Fetches top losers from Finviz using finvizfinance package.
    
    Returns:
        str: Formatted string containing top losers data
    """
    # Create a screener object
    foverview = Overview()
    
    # Use "Change" filter for top losers (stocks with highest negative change)
    filters_dict = {'Change': 'Top Losers'}  # This will filter for stocks with large negative change
    foverview.set_filter(filters_dict=filters_dict)
    
    # Get the data
    df = foverview.screener_view()
    
    # Sort by Change (%) in ascending order
    df = df.sort_values(by='Change', ascending=True)
    
    # Select top 10 records
    top_losers = df.head(10)
    
    # Format as string
    result = "Top Losers:\n"
    result += top_losers.to_string(index=False)
    
    return result

# Alternative approach using built-in finvizfinance methods
def get_top_gainers_alt():
    """
    Alternative method to fetch top gainers using finvizfinance's built-in functionality.
    
    Returns:
        str: Formatted string containing top gainers data
    """
    # Create a screener object
    foverview = Overview()
    
    # Get the data sorted by percent change (up)
    df = foverview.screener_view(order='Change', ascend=False)
    
    # Select top 10 records
    top_gainers = df.head(10)
    
    # Format as string
    result = "Top Gainers:\n"
    result += top_gainers.to_string(index=False)
    
    return result

def get_top_losers_alt():
    """
    Alternative method to fetch top losers using finvizfinance's built-in functionality.
    
    Returns:
        str: Formatted string containing top losers data
    """
    # Create a screener object
    foverview = Overview()
    
    # Get the data sorted by percent change (down)
    df = foverview.screener_view(order='Change', ascend=True)
    
    # Select top 10 records
    top_losers = df.head(10)
    
    # Format as string
    result = "Top Losers:\n"
    result += top_losers.to_string(index=False)
    
    return result

# Example usage
if __name__ == "__main__":
    try:
        # Use alternative methods which should work more reliably
        print(get_top_gainers_alt())
        print("\n")
        print(get_top_losers_alt())
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure you have installed the finvizfinance package: pip install finvizfinance")