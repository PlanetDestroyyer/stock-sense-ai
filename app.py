from flask import Flask, render_template, request, jsonify
import logging
import traceback
from typing import Dict, Any
from flask_compress import Compress
from flask_cors import CORS
from codes.main import agent_executor, process_agent_output
from codes.yahoo_finance_helper import ask_yahoo_finance_news
from codes.ticker_info import ticker_news
from codes.topMovers import get_top_gainers, get_top_losers
import requests
import pandas as pd
from datetime import datetime
import logging
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
# Initialize Flask app
app = Flask(__name__, static_url_path='/static')
Compress(app)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Alpha Vantage API Key
 # Replace with a valid key

# Base URL for Alpha Vantage API
BASE_URL = 'https://www.alphavantage.co/query'

# Function to get stock data for AAPL
def get_valid_data():
    ticker = "AAPL"
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': ticker,
        'interval': '5min',
        'outputsize': 'compact',
        'datatype': 'json',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'Error Message' in data:
            logger.error(f"API error for ticker {ticker}: {data['Error Message']}")
            return None
        if 'Information' in data and 'Thank you for using Alpha Vantage' in data['Information']:
            logger.error(f"Rate limit or key issue for ticker {ticker}: {data['Information']}")
            return None
        
        time_series_key = "Time Series (5min)"
        if time_series_key not in data:
            logger.error(f"No time series data for ticker {ticker}. Full response: {data}")
            return None
        
        df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for ticker {ticker}: {e}")
        return None
    except ValueError as e:
        logger.error(f"JSON decode error for ticker {ticker}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for ticker {ticker}: {e}")
        return None

@app.route('/')
def index():
    gainers = get_top_gainers()
    return render_template("index.html",gainers=gainers.to_dict(orient='records'))

@app.route('/api/market-data')
def get_market_data():
    data = get_valid_data()
    
    if data is None or data.empty:
        return jsonify({"error": "No data available for AAPL"}), 500
    
    labels = [timestamp.strftime("%H:%M") for timestamp in data.index]
    prices = data["4. close"].round(2).tolist()

    return jsonify({
        "labels": labels,
        "prices": prices,
        "ticker": "AAPL"
    })

@app.route('/top_movers')
def movers():
    gainers = get_top_gainers()
    losers = get_top_losers()
    return render_template(
        "top-movers.html", 
        gainers=gainers.to_dict(orient='records'), 
        losers=losers.to_dict(orient='records')
    )





@app.route('/ai_assistant', methods=['GET', 'POST'])
def assistant():
    if request.method == 'POST':
        try:
            # Get query from JSON or form data
            if request.is_json:
                query = request.json.get('query', '').strip()
            else:
                query = request.form.get('query', '').strip()

            if not query:
                return jsonify({"error": "Query is required"}), 400

            logging.info(f"Processing query: {query}")
            
            # Call your AI agent
            raw_response = agent_executor.invoke({"input": query})
            logging.info(f"Raw agent response: {raw_response}")

            # Process the response
            response = process_agent_output(raw_response)
            
            # Prepare standardized response format
            response_data = {
    "topic": response.get("topic"),
    "response": response.get("response"),
    "summary": response.get("summary"),
    "tools_used": response.get("tools_used", []),
    "links": response.get("links", []),
    "source": response.get("source", [])
}

            return jsonify({
                "response": response_data,
                "query": query
            })

        except Exception as e:
            logging.error(f"Error in AI assistant: {str(e)}")
            logging.error(traceback.format_exc())
            return jsonify({
                "error": f"An error occurred: {str(e)}"
            }), 500

    # GET request - show empty chat interface
    return render_template("ai-assistant.html")


def process_agent_output(raw_response: Dict[str, Any]) -> Any:
    """
    Process the raw response from the AI agent into a structured format.
    Modify this function according to your agent's response structure.
    """
    try:
        # Example processing - adjust based on your actual agent response
        if 'output' in raw_response:
            # Try to parse JSON if output is in JSON format
            if raw_response['output'].strip().startswith('```json'):
                import json
                json_str = raw_response['output'].replace('```json', '').replace('```', '').strip()
                return json.loads(json_str)
            return {"response": raw_response['output']}
        return {"response": str(raw_response)}
    except Exception as e:
        logging.error(f"Error processing agent output: {str(e)}")
        return {"response": str(raw_response), "error": "Could not process agent output"}



@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'POST':
        ticker = request.form.get('query')
        if not ticker:
            return render_template("news.html", error="Ticker is required", query="", news=[], price="N/A")
        try:
            response = ticker_news(ticker.upper())
            logger.info(f"ticker_news response for {ticker}: {response}")
            if response is None or not isinstance(response, list):
                return render_template("news.html", error=f"No data found for {ticker}", query=ticker, news=[], price="N/A")
            news, price = response
            return render_template("news.html", ticker=ticker.upper(), news=news, price=price, query=ticker)
        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}", exc_info=True)
            return render_template("news.html", error=f"Error fetching data for {ticker}", query=ticker, news=[], price="N/A")
    return render_template("news.html", query="", news=[], price="N/A")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)