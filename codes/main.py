import os
from codes.news import ask_duckduckgo
from codes.ticker_info import stock_info, ticker_news
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from codes.llm import llm
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import Tool
from typing import Optional, List
import traceback
from pydantic import ValidationError



ask_yahoo_finance_news = YahooFinanceNewsTool()

# Set USER_AGENT to avoid web scraping issues
os.environ["USER_AGENT"] = "StockSenseAI/1.0 (stock-sense-ai@example.com)"

class Output(BaseModel):
    topic: str = Field(..., description="The main topic of the query")
    source: List[str] = Field(default_factory=list, description="Sources used for the response")
    tools_used: List[str] = Field(default_factory=list, description="List of tools used to generate the response")
    response: str = Field(..., description="The main response text")
    links: List[str] = Field(default_factory=list, description="Relevant links")
    agent_scratchpad: str = Field("", description="Agent's working notes")
    summary: str = Field(..., description="Brief summary of the response")

# Initialize Pydantic parser
parser = PydanticOutputParser(pydantic_object=Output)

# Define prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a financial assistant that answers questions about companies and markets. 
        You MUST use the provided tools to fetch accurate, current information for EVERY query. Do NOT rely on your internal knowledge or generate answers without calling at least one tool.

        Guidelines:
        - For leadership questions (e.g., CEO), use 'ask_duckduckgo'.
        - For market-wide queries (e.g., top gainers or losers), use 'ask_duckduckgo'.
        - For ticker-specific queries, use 'stock_info', 'ticker_news', or 'ask_yahoo_finance_news'.
        - Always call at least one tool to gather data before responding.
        - Summarize tool outputs clearly in the 'response' and 'summary' fields.
        - Include relevant links and sources from tool outputs in the 'links' and 'source' fields.
        - If no links or sources are available, use empty lists (`[]`).
        - If no specific topic is identified, use a relevant default based on the query.
        - Format your final output as a JSON object matching the structure below.

        {format_instruction}"""),
        ("human", "Answer the query by using the appropriate tools to fetch current data: {input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instruction=parser.get_format_instructions())

# Define tools with explicit descriptions
tools = [
    Tool(
        name="ask_duckduckgo",
        func=ask_duckduckgo,
        description="Search the web for factual information, such as company leadership (e.g., CEO), general company details, or market-wide data (e.g., top stock market gainers or losers)."
    ),
    Tool(
        name="ask_yahoo_finance_news",
        func=ask_yahoo_finance_news,
        description="Fetch recent news articles related to a specific stock ticker's market performance."
    ),
    Tool(
        name="stock_info",
        func=stock_info,
        description="Retrieve financial data or metrics for a specific stock ticker (e.g., price, volume, P/E ratio)."
    ),
    Tool(
        name="ticker_news",
        func=ticker_news,
        description="Get the latest news articles related to a specific stock ticker."
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
    verbose=False,  # Enable for debugging
    max_iterations=6,  # Allow more iterations for complex queries
    handle_parsing_errors=True,  # Better error handling
)




if __name__ == "__main__":
    try:
        query = "Tell me about Tesla stock performance"
        print(f"Testing query: {query}")
        raw_response = agent_executor.invoke({"input": query})
        print(f"Raw agent response: {raw_response}")
        response = process_agent_output(raw_response)
        print("Processed Response:")
        print(response)
    except Exception as e:
        print(f"Test execution failed: {e}")
        print(traceback.format_exc())
