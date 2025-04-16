from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
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
def ask_gemini(query):
    """
    Ask the Gemini agent a question and get the response.
    """
    response = chain.invoke({"input": query})
    return response


if __name__ == "__main__":
    # Example usage
    pass