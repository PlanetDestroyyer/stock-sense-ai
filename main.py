from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Sample response models
class TopMoverResponse(BaseModel):
    stock: str
    growth_percentage: str
    price: str

class NewsImpactResponse(BaseModel):
    stock: str
    news: str
    sentiment: str

class AiAssistantResponse(BaseModel):
    question: str
    answer: str

class WebPageResponse(BaseModel):
    url: str
    description: str


# Endpoint 1: Top Mover
@app.get("/top_mover/", response_model=TopMoverResponse)
async def top_mover():
    # For now, using mock data until real data fetch logic is implemented
    return {"stock": "AAPL", "growth_percentage": "5.2%", "price": "150.00 USD"}

# Endpoint 2: News Impact
@app.get("/news_impact/", response_model=NewsImpactResponse)
async def news_impact():
    # For now, using mock data
    return {"stock": "AAPL", "news": "Apple announces new product.", "sentiment": "positive"}

# Endpoint 3: AI Assistant
@app.get("/ai_assistant/", response_model=AiAssistantResponse)
async def ai_assistant(query: str):
    # For now, returning a mocked response
    return {"question": query, "answer": "This is a mock response to your query."}

# Endpoint 4: Web Page
@app.get("/web_page/", response_model=WebPageResponse)
async def web_page():
    # For now, returning mock data with a link to your project page
    return {"url": "http://example.com", "description": "This is the web page for the Stock Market Assistant project."}
