import time
import requests
import talib
import numpy as np

# Constants
API_BASE_URL = 'https://api.coindcx.com'
SYMBOL = 'BTCINR'
INTERVAL = '1m'
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_QUANTITY = 0.001  # Quantity of the asset to trade

# CoinDCX API endpoints
ENDPOINT_TICKER = '/exchange/ticker'
ENDPOINT_TRADE_HISTORY = '/exchange/tradehistory'

# Neural Network model - replace with your own implementation
class NeuralNetwork:
    def __init__(self):
        pass
    
    def predict(self, data):
        # Make predictions based on the input data
        return 0  # Replace with your own prediction logic


# Initialize Neural Network model
model = NeuralNetwork()

def get_latest_price():
    response = requests.get(API_BASE_URL + ENDPOINT_TICKER, params={'symbol': SYMBOL})
    if response.status_code == 200:
        ticker_data = response.json()
        return float(ticker_data['last_price'])
    else:
        print('Failed to get the latest price')
        return None

def get_historical_data():
    response = requests.get(API_BASE_URL + ENDPOINT_TRADE_HISTORY, params={'symbol': SYMBOL, 'interval': INTERVAL})
    if response.status_code == 200:
        trade_history = response.json()
        prices = [float(trade['p']) for trade in trade_history]
        return prices
    else:
        print('Failed to get historical data')
        return []

def calculate_rsi(prices):
    np_prices = np.array(prices)
    rsi = talib.RSI(np_prices, RSI_PERIOD)
    return rsi[-1] if len(rsi) > 0 else None

def execute_trade(action):
    # Replace with your own trade execution logic
    if action == 'buy':
        print('Executing buy order')
    elif action == 'sell':
        print('Executing sell order')
    else:
        print('Invalid action')

def main():
    while True:
        latest_price = get_latest_price()
        if latest_price is not None:
            historical_data = get_historical_data()
            rsi = calculate_rsi(historical_data)

            if rsi:
                prediction = model.predict([rsi])  # Use Neural Network model to predict action
                if prediction > 0:
                    execute_trade('buy')
                elif prediction < 0:
                    execute_trade('sell')

        time.sleep(60)  # Wait for 1 minute before checking again

if __name__ == '__main__':
    main()
