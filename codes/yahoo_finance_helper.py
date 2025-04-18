from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from codes.llm import llm
from langchain.tools import tool
yfinacen_tools = [YahooFinanceNewsTool()]


agent_chain = initialize_agent(
    yfinacen_tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)


@tool
def ask_yahoo_finance_news(stock: str) -> str:
    """
    Ask Yahoo Finance for the latest news about a stock."""
    response = agent_chain.invoke(stock)
    return response

if __name__ == "__main__":
    # Example usage
    output = ask_yahoo_finance_news("What is the latest news about Apple?")
    print(output)