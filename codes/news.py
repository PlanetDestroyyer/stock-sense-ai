from langchain_community.tools import DuckDuckGoSearchResults

duckgo_search = DuckDuckGoSearchResults()

def ask_duckduckgo(query):
    """
    Ask the DuckDuckGo search agent a question and get the response.
    """
    response = duckgo_search.run(query)
    return response

if __name__ == "__main__":
    # Example usage
    pass