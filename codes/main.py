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
        Use the provided tools to fetch accurate, current information.
        
        Guidelines:
        - For leadership questions (e.g., CEO), prioritize 'ask_duckduckgo'.
        - For market-wide queries (e.g., top gainers or losers), use 'ask_duckduckgo'.
        - For ticker-specific queries, use 'stock_info', 'ticker_news', or 'ask_yahoo_finance_news'.
        - Always use at least one tool to gather information.
        - Never return generic or template responses.
        - Summarize tool outputs clearly in the 'response' and 'summary' fields.
        - Include relevant links and sources from tool outputs in the 'links' and 'source' fields.
        - If no links or sources are available, use empty lists (`[]`).
        - If no specific topic is identified, use a relevant default based on the query.
        
        Return your final output as a JSON object matching the format below. Ensure all fields are populated, using defaults where necessary.

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
    verbose=False,  # Enable for debugging
    max_iterations=6,  # Allow more iterations for complex queries
    handle_parsing_errors=True,  # Better error handling
)


def process_agent_output(raw_response):
    try:
        print(f"Processing raw response: {raw_response}")
        
        # Initialize default Output object
        default_output = Output(
            topic="Stock Analysis",
            source=[],
            tools_used=[],
            response="",
            links=[],
            summary="Analysis completed based on available data.",
            agent_scratchpad=None
        )

        # Extract tools used from intermediate_steps
        tools_used = []
        tool_outputs = []
        if isinstance(raw_response, dict) and "intermediate_steps" in raw_response:
            for step in raw_response.get("intermediate_steps", []):
                if len(step) >= 2 and hasattr(step[0], "tool"):
                    tools_used.append(step[0].tool)
                    # Extract tool output (e.g., links, text)
                    tool_output = step[1] if len(step) > 1 else None
                    if tool_output:
                        tool_outputs.append(tool_output)

        # Case 1: Output is a JSON string
        if isinstance(raw_response, dict) and "output" in raw_response:
            output = raw_response["output"]
            if isinstance(output, str):
                try:
                    # Try parsing as JSON
                    if output.strip().startswith('```json'):
                        output = output.replace('```json', '').replace('```', '').strip()
                    parsed_output = parser.parse(output)
                    # Update defaults with parsed values
                    default_output = parsed_output
                    default_output.tools_used = tools_used or default_output.tools_used
                    default_output.source = default_output.source or [t for t in tools_used]
                    return default_output
                except ValidationError as ve:
                    print(f"Pydantic validation error: {ve}")
                    default_output.response = output
                    default_output.error = f"Invalid output format: {str(ve)}"
                except json.JSONDecodeError as je:
                    print(f"JSON decode error: {je}")
                    default_output.response = output
                    default_output.error = f"Failed to parse JSON: {str(je)}"
            elif isinstance(output, dict):
                # Case 2: Output is a dictionary
                try:
                    parsed_output = Output(**output)
                    default_output = parsed_output
                    default_output.tools_used = tools_used or default_output.tools_used
                    default_output.source = default_output.source or [t for t in tools_used]
                    return default_output
                except ValidationError as ve:
                    print(f"Pydantic validation error for dict: {ve}")
                    default_output.response = str(output)
                    default_output.error = f"Invalid output structure: {str(ve)}"
            else:
                # Case 3: Output is neither string nor dict
                default_output.response = str(output)
        else:
            # Case 4: No valid output key
            default_output.response = str(raw_response)

        # Extract links and sources from tool outputs
        for tool_output in tool_outputs:
            if isinstance(tool_output, dict):
                if "links" in tool_output:
                    default_output.links.extend(tool_output.get("links", []))
                if "source" in tool_output:
                    default_output.source.extend(tool_output.get("source", []))
            elif isinstance(tool_output, str):
                # Extract URLs from text (basic regex for simplicity)
                import re
                urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', tool_output)
                default_output.links.extend(urls)

        # Generate summary if none provided
        if not default_output.summary and default_output.response:
            default_output.summary = default_output.response[:100] + "..." if len(default_output.response) > 100 else default_output.response

        # Ensure tools_used and source are populated
        default_output.tools_used = tools_used or default_output.tools_used
        default_output.source = default_output.source or [t for t in tools_used]

        # Clean up: Remove duplicates and None values
        default_output.links = list(set([l for l in default_output.links if l]))
        default_output.source = list(set([s for s in default_output.source if s]))
        default_output.tools_used = list(set([t for t in default_output.tools_used if t]))

        return default_output

    except Exception as e:
        print(f"Error in process_agent_output: {e}")
        print(traceback.format_exc())
        return Output(
            topic="Error",
            source=[],
            tools_used=[],
            response=f"An error occurred while processing the response: {str(e)}",
            links=[],
            summary="Error during response processing.",
            agent_scratchpad=None
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