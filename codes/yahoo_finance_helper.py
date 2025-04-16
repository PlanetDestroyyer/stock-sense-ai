from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from llm import llm
yfinacen_tools = [YahooFinanceNewsTool()]


agent_chain = initialize_agent(
    yfinacen_tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)



def ask_yahoo_finance_news(query):
    """
    Ask the Yahoo Finance News agent a question and get the response.
    """
    response = agent_chain.run(query)
    return response

if __name__ == "__main__":
    # Example usage
    pass