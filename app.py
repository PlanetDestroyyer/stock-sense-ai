from flask_compress import Compress
from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory, Response
import os

app = Flask(__name__, static_url_path='/static')

Compress(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/top_movers')
def movers():
    return render_template("top_movers.html")

@app.route('/ai_assistant')
def assistant():
    return render_template("ai_assistant.html")

@app.route('/news_impact')
def news():
    return render_template("news_inmpact.html")


if __name__ == '__main__':
    app.run(debug=True)
