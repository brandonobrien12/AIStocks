from flask import Flask, render_template
from threading import Thread
from time import sleep
from tradingview_ta import *

app = Flask(__name__)

results = {}  # Global variable to store results

@app.route('/')
def index():
    return render_template('index.html', results=results)

def run_tradingview_ta_periodically():
    global results
    while True:
        results = run_tradingview_ta_script()
        sleep(1)  # Sleep for 1 seconds

def run_tradingview_ta_script():
    new_results = {}
    symbols_nasdaq = ["qqq", "tsla", "aapl", "mara", "nvda", "riot", "hut", "coin"]
    
    for symbol in symbols_nasdaq:
        handler = TA_Handler(
            symbol=symbol,
            screener="america",
            exchange="NASDAQ",
            interval=Interval.INTERVAL_15_MINUTES,
        )

        analysis = handler.get_analysis()

        result_summary = {
            'summary': analysis.summary,
            'RSI': analysis.indicators.get('RSI'),
            'Momentum': analysis.indicators.get('Mom'),
            'open': analysis.indicators.get('open')
        }

        new_results[symbol] = result_summary
        #print("Open:", analysis.indicators['open'])
        
    return new_results

if __name__ == '__main__':
    # Start the periodic task in a separate thread
    thread = Thread(target=run_tradingview_ta_periodically)
    thread.start()

    # Run the Flask application
    app.run(debug=True)
