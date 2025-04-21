from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain.tools import tool

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key = os.getenv("GROQ_API_KEY"),
    
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