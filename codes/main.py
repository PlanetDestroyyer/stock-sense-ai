import os
from news import ask_duckduckgo
from ticker_info import stock_info, ticker_news
from yahoo_finance_helper import ask_yahoo_finance_news
from llm import llm
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import Tool
from typing import Optional

# Set USER_AGENT to avoid web scraping issues
os.environ["USER_AGENT"] = "StockSenseAI/1.0 (stock-sense-ai@example.com)"

class Output(BaseModel):
    topic: Optional[str] = None
    source: Optional[list[str]] = None
    tools_used: Optional[list[str]] = None
    response: Optional[str] = None
    links: Optional[list[str]] = None
    agent_scratchpad: Optional[str] = None
    summary: Optional[str] = None  # Made optional to avoid validation errors

# Initialize Pydantic parser
parser = PydanticOutputParser(pydantic_object=Output)

# Define prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a financial assistant that answers questions about companies and markets. Use the provided tools to fetch accurate information. For leadership questions (e.g., CEO), prioritize 'ask_duckduckgo'. For market-wide queries (e.g., top gainers or losers), use 'ask_duckduckgo' with precise queries like 'top stock market gainers today' or 'top stock market losers today'. For ticker-specific queries, use 'stock_info', 'ticker_news', or 'ask_yahoo_finance_news'. Correct typos in queries (e.g., 'lossers' to 'losers'). Wrap the output in this format: \n{format_instruction}"),
        ("human", "Answer the query directly and concisely. If a stock ticker is provided, fetch news or details as requested. For general company or market questions, use appropriate tools to provide accurate answers. \nQuery: {input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instruction=parser.get_format_instructions())

# Define tools with explicit descriptions
tools = [
    Tool(
        name="ask_duckduckgo",
        func=ask_duckduckgo,
        description="Search the web for factual information, such as company leadership (e.g., CEO), general company details, or market-wide data (e.g., top stock market gainers or losers). Use precise queries for market queries, like 'top stock market losers today'."
    ),
    Tool(
        name="ask_yahoo_finance_news",
        func=ask_yahoo_finance_news,
        description="Fetch recent news articles related to a specific stock ticker's market performance. Use only for ticker-specific queries."
    ),
    Tool(
        name="stock_info",
        func=stock_info,
        description="Retrieve financial data or metrics for a specific stock ticker (e.g., price, volume, P/E ratio). Use only for ticker-specific queries."
    ),
    Tool(
        name="ticker_news",
        func=ticker_news,
        description="Get the latest news articles related to a specific stock ticker. Use only for ticker-specific queries."
    ),
]

# Create agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt_template,
)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Enable for debugging
    max_iterations=6,  # Allow more iterations for complex queries
)

# Pre-process query to correct typos
def preprocess_query(query: str) -> str:
    query = query.lower().strip()
    if "lossers" in query:
        query = query.replace("lossers", "losers")
    if "top loser" in query or "top losers" in query:
        return f"top stock market losers today"
    return query

# Process agent output
def process_agent_output(raw_response):
    if "output" in raw_response and raw_response["output"]:
        try:
            return parser.parse(raw_response["output"])
        except Exception as e:
            return Output(
                topic="Error",
                source=["Agent"],
                tools_used=None,
                response=f"Failed to parse output: {str(e)}",
                links=None,
                agent_scratchpad=str(raw_response),
                summary="Output parsing failed."
            )
    return Output(
        topic="Error",
        source=["Agent"],
        tools_used=None,
        response="No valid output from agent",
        links=None,
        agent_scratchpad=str(raw_response),
        summary="Agent did not produce a valid output."
    )

# Main execution
if __name__ == "__main__":
    try:
        query = "Tell me about Tesla stock performance?"
        corrected_query = preprocess_query(query)
        raw_response = agent_executor.invoke({
            "input": query,
            "chat_history": "",
            "agent_scratchpad": "",
        })
        response = process_agent_output(raw_response)
        print("Response:")
        print(response)
    except Exception as e:
        print(Output(
            topic="Error",
            source=["Agent"],
            tools_used=None,
            response=f"Agent execution failed: {str(e)}",
            links=None,
            agent_scratchpad=None,
            summary="Agent execution failed."
        ))