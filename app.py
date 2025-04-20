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
from codes.compare_stocks import compare_stocks
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
            
            # Validate response schema
            required_fields = ["topic", "response", "summary", "tools_used", "links", "source"]
            for field in required_fields:
                if field not in response:
                    response[field] = [] if field in ["tools_used", "links", "source"] else ""
            
            # Prepare standardized response format
            response_data = {
                "topic": response["topic"],
                "response": response["response"],
                "summary": response["summary"],
                "tools_used": response["tools_used"],
                "links": response["links"],
                "source": response["source"]
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

import json
import logging
from typing import Dict, Any

def process_agent_output(raw_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process the raw response from the AI agent into a structured format.
    Ensures consistent output schema with default values for missing fields.
    """
    try:
        # Initialize default response structure
        processed_response = {
            "topic": "General",
            "response": "",
            "summary": "",
            "tools_used": [],
            "links": [],
            "source": []
        }

        # Case 1: JSON-formatted output
        if isinstance(raw_response, dict) and 'output' in raw_response:
            output = raw_response['output']
            if isinstance(output, str) and output.strip().startswith('```json'):
                # Strip markdown and parse JSON
                json_str = output.replace('```json', '').replace('```', '').strip()
                try:
                    json_data = json.loads(json_str)
                    # Update processed_response with JSON data
                    processed_response.update({
                        "topic": json_data.get("topic", "General"),
                        "response": json_data.get("response", ""),
                        "summary": json_data.get("summary", ""),
                        "tools_used": json_data.get("tools_used", []),
                        "links": json_data.get("links", []),
                        "source": json_data.get("source", [])
                    })
                    return processed_response
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to parse JSON output: {str(e)}")
                    processed_response["response"] = output
                    processed_response["error"] = "Invalid JSON format in agent output"
            else:
                # Non-JSON output
                processed_response["response"] = str(output)
        else:
            # Case 2: Raw response is not a dict or lacks 'output'
            processed_response["response"] = str(raw_response)

        # Extract metadata if present (e.g., from agent_scratchpad)
        if isinstance(raw_response, dict):
            metadata = raw_response.get('metadata', {})
            processed_response.update({
                "topic": metadata.get("topic", processed_response["topic"]),
                "summary": metadata.get("summary", processed_response["summary"]),
                "tools_used": metadata.get("tools_used", processed_response["tools_used"]),
                "links": metadata.get("links", processed_response["links"]),
                "source": metadata.get("source", processed_response["source"])
            })

        # Clean up: Remove null or empty lists, ensure types
        for key in ["tools_used", "links", "source"]:
            if not processed_response[key]:
                processed_response[key] = []
            elif not isinstance(processed_response[key], list):
                processed_response[key] = [processed_response[key]]

        # Generate a summary if none provided
        if not processed_response["summary"] and processed_response["response"]:
            processed_response["summary"] = processed_response["response"][:100] + "..." if len(processed_response["response"]) > 100 else processed_response["response"]

        return processed_response

    except Exception as e:
        logging.error(f"Error processing agent output: {str(e)}")
        return {
            "topic": "Error",
            "response": str(raw_response),
            "summary": "Failed to process response",
            "tools_used": [],
            "links": [],
            "source": [],
            "error": f"Processing error: {str(e)}"
        }



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





@app.route('/comparison')
def home():
    return render_template('comparison.html')


@app.route('/compare', methods=['POST'])
def compare():
    try:
        data = request.json
        ticker1 = data.get('ticker1')
        ticker2 = data.get('ticker2')
        print(f"Received tickers: {ticker1}, {ticker2}") # Debug

        if not ticker1 or not ticker2:
            return jsonify({'error': 'Both tickers are required'}), 400

        result = compare_stocks(ticker1, ticker2)
        return jsonify({'result': result})
    except Exception as e:
        print(f"Error in /compare: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)