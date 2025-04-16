from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain.tools import tool

llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="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",
    
)
# Define a prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{input}"),
    ]
)
# Create a chain with the prompt template
chain = prompt_template | llm
# Define a function to use the chain

@tool
def ask_groq(query):
    """
    Ask the Gemini agent a question and get the response.
    """
    response = chain.invoke({"input": query})
    return response


if __name__ == "__main__":
    # Example usage
    pass