from flask import Flask, render_template
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime, timedelta
import os
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data')
def data():
    # Set up the stock symbol and date range
    symbol = 'AAPL'  # Replace with the desired stock symbol
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    # Fetch data from Yahoo Finance API
    stock_data = yf.download(symbol, start=start_date, end=end_date)

    # Reset the index to convert dates to a column
    stock_data.reset_index(inplace=True)
    stock_data['Date'] = stock_data['Date'].dt.strftime('%Y-%m-%d')
    if not os.path.exists('static'):
        os.makedirs('static')

    # Generate a plot using matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Date'], stock_data['Close'])
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title(f'{symbol} Stock Price Over the Last 30 Days')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/stock_price.png')

    # Convert the DataFrame to a dictionary for passing to the template
    data_dict = stock_data.to_dict('records')

    return render_template('data.html', data=data_dict, symbol=symbol)

if __name__ == '__main__':
    app.run(debug=True)

@freezer.register_generator
def url_generator():
    yield '/'

freezer.freeze()