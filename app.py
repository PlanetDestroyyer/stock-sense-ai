from flask_compress import Compress
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory, Response
import os
from codes.main import agent_executor
from codes.yahoo_finance_helper import ask_yahoo_finance_news
from codes.ticker_info import ticker_news
app = Flask(__name__, static_url_path='/static')

Compress(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/top_movers')
def movers():
    return render_template("top_movers.html")

@app.route('/ai_assistant',methods=['GET', 'POST'])
def assistant():
    if request.method == 'POST':
        query = request.form['query']
        response = agent_executor.invoke({
            "input": query
        })
        return render_template("ai_assistant.html", response=response, query=query)
    else:
        # Handle GET request
        return render_template("ai_assistant.html")
    return render_template("ai_assistant.html")

@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'POST':
        query = request.form['query']
        response = ticker_news(query)
        return render_template("news.html", response=response, query=query)
    
    return render_template("news.html")


if __name__ == '__main__':
    app.run(debug=True)
