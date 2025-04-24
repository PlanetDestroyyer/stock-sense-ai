from flask import Flask, render_template, request, jsonify
from finvizfinance.screener.overview import Overview
import logging
import traceback
from typing import Dict, Any
from flask_compress import Compress
from flask_cors import CORS
from codes.main import agent_executor, process_agent_output
from codes.yahoo_finance_helper import ask_yahoo_finance_news
from codes.ticker_info import ticker_news
from codes.topMovers import get_top_losers, get_new_top_gainers
from codes.compare_stocks import compare_stocks
import requests
import pandas as pd
from datetime import datetime
import logging
import os
import traceback
from dotenv import load_dotenv
import yfinance as yf
from datetime import datetime, timedelta

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# Initialize Flask app
app = Flask(__name__, static_url_path='/static')
Compress(app)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_valid_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1d", interval="5m")
        if df.empty:
            print(f"No data returned for ticker {ticker}")
            return None
        df.index = pd.to_datetime(df.index)
        df = df[['Close']].round(2)
        return df
    except Exception as e:
        print(f"Error fetching data for ticker {ticker}: {e}")
        return None

def get_top_gainers():
    try:
        screener = Overview()
        # Set filter for significant gainers (adjust threshold if needed)
        screener.set_filter(filters_dict={'Change': 'Up 20%'})
        df = screener.screener_view()
        if df.empty:
            print("No gainers found from Finviz")
            return []
        # Sort by Change and take top 4
        top_gainers = df.sort_values(by='Change', ascending=False).head(3)
        gainers = []
        for _, row in top_gainers.iterrows():
            ticker = row['Ticker']
            # Fetch volume from yfinance for consistency
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(period="1d")
                volume = f'{int(data["Volume"][-1] / 1_000_000)}M' if not data.empty else 'N/A'
            except:
                volume = 'N/A'
            gainers.append({
                'Ticker': ticker,
                'Change': f'+{row["Change"]:.2f}%' if isinstance(row["Change"], (int, float)) else row["Change"],
                'Company': row['Company'],
                'Volume': volume
            })
        return gainers
    except Exception as e:
        print(f"Error fetching gainers from Finviz: {e}")
        return []

def get_market_news():
    try:
        url = f"https://newsapi.org/v2/everything?q=stock%20market%20OR%20finance&apiKey={NEWS_API_KEY}&language=en&sortBy=publishedAt&pageSize=5"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('status') != 'ok':
            print(f"NewsAPI error: {data.get('message')}")
            return []
        articles = data.get('articles', [])
        news = [
            {
                'title': article['title'],
                'source': article['source']['name'],
                'description': article['description'] or '',
                'url': article['url']
            }
            for article in articles
        ]
        return news
    except Exception as e:
        print(f"Error fetching news: {e}")
        # Fallback mock news
        # "No news available at the moment."

@app.route('/api/market-data')
def get_market_data():
    indices = [
        {'ticker': '^GSPC', 'name': 'S&P 500'},
        {'ticker': '^IXIC', 'name': 'NASDAQ'},
        {'ticker': '^DJI', 'name': 'Dow Jones'}
    ]
    result = {
        'labels': [],
        'datasets': [],
        'current_prices': []
    }
    for index in indices:
        data = get_valid_data(index['ticker'])
        if data is None or data.empty:
            return jsonify({"error": f"No data available for {index['name']}"}), 500
        if not result['labels']:
            result['labels'] = [timestamp.strftime("%H:%M") for timestamp in data.index]
        prices = data["Close"].tolist()
        current_price = data["Close"].iloc[-1]
        result['datasets'].append({
            'name': index['name'],
            'prices': prices
        })
        result['current_prices'].append({
            'name': index['name'],
            'price': current_price
        })
    return jsonify(result)

@app.route('/')
def dashboard():
    gainers = get_top_gainers()
    news = get_market_news()
    return render_template('index.html', gainers=gainers, news=news)



@app.route('/top_movers')
def movers():
    gainers = get_new_top_gainers()
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