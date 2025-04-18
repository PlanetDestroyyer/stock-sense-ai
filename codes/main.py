import os
from codes.news import ask_duckduckgo
from codes.ticker_info import stock_info, ticker_news
from codes.yahoo_finance_helper import ask_yahoo_finance_news
from codes.llm import llm
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import Tool
from typing import Optional, List
import traceback

# Set USER_AGENT to avoid web scraping issues
os.environ["USER_AGENT"] = "StockSenseAI/1.0 (stock-sense-ai@example.com)"

class Output(BaseModel):
    topic: Optional[str] = Field(None, description="The main topic of the query")
    source: Optional[List[str]] = Field(None, description="Sources used for the response")
    tools_used: Optional[List[str]] = Field(None, description="List of tools used to generate the response")
    response: str = Field(..., description="The main response text")
    links: Optional[List[str]] = Field(None, description="Relevant links")
    agent_scratchpad: Optional[str] = Field(None, description="Agent's working notes")
    summary: Optional[str] = Field(None, description="Brief summary of the response")

# Initialize Pydantic parser
parser = PydanticOutputParser(pydantic_object=Output)

# Define prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a financial assistant that answers questions about companies and markets. 
        Use the provided tools to fetch accurate information.
        
        For leadership questions (e.g., CEO), prioritize 'ask_duckduckgo'.
        For market-wide queries (e.g., top gainers or losers), use 'ask_duckduckgo'.
        For ticker-specific queries, use 'stock_info', 'ticker_news', or 'ask_yahoo_finance_news'.
        
        Always provide detailed, specific information based on current data.
        Never return generic template responses.
        Always use at least one tool to gather information before responding.
        
        Wrap your final output in the format specified by the format instructions.

        {format_instruction}"""),
        ("human", "Answer the query directly and concisely based on current data. If a stock ticker is provided, fetch news or details as requested: {input}"),
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
    verbose=True,  # Enable for debugging
    max_iterations=6,  # Allow more iterations for complex queries
    handle_parsing_errors=True,  # Better error handling
)

# Process agent output
def process_agent_output(raw_response):
    try:
        print(f"Processing raw response: {raw_response}")
        
        # If raw_response is already a dictionary with Output structure
        if isinstance(raw_response, dict) and "output" in raw_response:
            try:
                # Try to parse the structured output
                if isinstance(raw_response["output"], str):
                    return parser.parse(raw_response["output"])
                # If output is already a dict, convert to Output model
                elif isinstance(raw_response["output"], dict):
                    return Output(**raw_response["output"])
            except Exception as parsing_error:
                print(f"Error parsing output: {parsing_error}")
                print(traceback.format_exc())
                
                # Return a simplified Output with the raw response
                return Output(
                    topic="Stock Analysis",
                    source=["Agent Analysis"],
                    tools_used=[],
                    response=str(raw_response["output"]),
                    links=None,
                    summary="Analysis completed with parsing issues."
                )
        
        # If we have intermediate_steps, extract tool usage
        tools_used = []
        if "intermediate_steps" in raw_response:
            for step in raw_response["intermediate_steps"]:
                if len(step) >= 2 and hasattr(step[0], "tool"):
                    tools_used.append(step[0].tool)
        
        # Handle different response formats
        if "output" in raw_response:
            response_text = raw_response["output"]
        elif "response" in raw_response:
            response_text = raw_response["response"]
        else:
            response_text = str(raw_response)
            
        # Create a clean Output object
        return Output(
            topic="Stock Analysis",
            source=["Financial Data Tools"],
            tools_used=tools_used,
            response=response_text,
            links=None,
            summary="Analysis completed based on available market data."
        )
    
    except Exception as e:
        print(f"Error in process_agent_output: {e}")
        print(traceback.format_exc())
        return Output(
            topic="Error",
            source=["Agent"],
            tools_used=None,
            response=f"An error occurred while processing the response: {str(e)}",
            links=None,
            summary="Error during response processing."
        )

# Main execution for testing
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