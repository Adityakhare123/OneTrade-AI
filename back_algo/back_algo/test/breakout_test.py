import requests
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import time
from talib import RSI

# Constants
PAIR = 'BTCINR'
WINDOW_SIZE = 14
BREAKOUT_THRESHOLD = 1.01
RSI_OVERBOUGHT_THRESHOLD = 70
RSI_OVERSOLD_THRESHOLD = 30
TRADE_QUANTITY = 0.001

# Coindcx API endpoints
PRICE_ENDPOINT = 'https://public.coindcx.com/market_data/trade_history'
ORDER_ENDPOINT = 'https://api.coindcx.com/exchange/v1/orders/create_market_order'

# Fetching data
def fetch_data():
    params = {'pair': PAIR}
    response = requests.get(PRICE_ENDPOINT, params=params)
    data = json.loads(response.text)

    # Creating pandas dataframe
    df = pd.DataFrame(data)
    df = df.astype(float)

    # Extracting closing price data
    close_data = df['price'].to_numpy()
    close_data = np.reshape(close_data, (-1, 1))

    # Calculating RSI data
    rsi_data = RSI(close_data, WINDOW_SIZE)

    # Scaling data between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    close_data = scaler.fit_transform(close_data)
    rsi_data = scaler.fit_transform(rsi_data.reshape(-1, 1))

    return close_data, rsi_data, scaler

# Trading function
def trade():
    close_data, rsi_data, scaler = fetch_data()

    # Preparing training and testing datasets
    training_data_len = int(np.ceil(len(close_data) * 0.7))
    test_data_len = len(close_data) - training_data_len
    train_data = close_data[0:training_data_len, :]
    rsi_train_data = rsi_data[0:training_data_len, :]

    # Creating training data
    X_train = []
    y_train = []
    for i in range(60, len(train_data)):
        X_train.append(np.concatenate((train_data[i-60:i, 0], rsi_train_data[i-60:i, 0]), axis=0))
        y_train.append(train_data[i, 0])

    # Converting training data to numpy arrays
    X_train, y_train = np.array(X_train), np.array(y_train)

    # Creating LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    # Compiling model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Training model
    model.fit(X_train, y_train, epochs=10, batch_size=32)

    # Creating test data
    test_data = close_data[training_data_len - 60:, :]
    rsi_test_data = rsi_data[training_data_len - 60:, :]

    # Creating X_test and y_test
    X_test = []
    y_test = close_data[training_data_len:, :]
    for i in range(60, len(test_data)):
        X_test.append(np.concatenate((test_data[i-60:i, 0], rsi_test_data[i-60:i, 0]), axis=0))
        y_test.append(test_data[i, 0])

    # Converting test data to numpy arrays
    X_test, y_test = np.array(X_test), np.array(y_test)

    # Reshaping X_test for LSTM input
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Predicting prices using the model
    predicted_prices = model.predict(X_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)

    # Getting the last closing price
    last_price = float(requests.get(PRICE_ENDPOINT, params={'pair': PAIR}).json()[0]['price'])

    # Calculating RSI of last closing price
    last_price_rsi = RSI(np.array([[last_price]]), WINDOW_SIZE)[-1][0]

    # Checking for breakout
    if predicted_prices[-1] > (BREAKOUT_THRESHOLD * last_price):
    # Checking for overbought condition
        if last_price_rsi > RSI_OVERBOUGHT_THRESHOLD:
        # Selling
            params = {
            'market': PAIR,
            'side': 'sell',
            'quantity': TRADE_QUANTITY
            }
            # response = requests.post(ORDER_ENDPOINT, data=params)
            # print(response.json())
            print(params)
        else:
            print('Not overbought, waiting for RSI to cross overbought threshold')
    else:
    # Checking for oversold condition
        if last_price_rsi < RSI_OVERSOLD_THRESHOLD:
            # Buying
            params = {
            'market': PAIR,
            'side': 'buy',
            'quantity': TRADE_QUANTITY
            }
            # response = requests.post(ORDER_ENDPOINT, data=params)
            # print(response.json())
            print(params)
        else:
            print('Not oversold, waiting for RSI to cross oversold threshold')

    # Waiting for 10 seconds before checking again
    time.sleep(10)

trade()