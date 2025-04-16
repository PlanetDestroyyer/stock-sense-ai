from langchain_community.tools import DuckDuckGoSearchResults
from langchain.tools import tool
duckgo_search = DuckDuckGoSearchResults()

@tool
def ask_duckduckgo(query):
    """
    Ask DuckDuckGo a question and get the response."""

    response = duckgo_search.run(query)
    return response

if __name__ == "__main__":
    # Example usage
    pass