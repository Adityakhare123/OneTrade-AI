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
import matplotlib.pyplot as plt

# Constants
PAIR = 'I-BTC_INR'
WINDOW_SIZE = 14
BREAKOUT_THRESHOLD = 1.01
RSI_OVERBOUGHT_THRESHOLD = 50
RSI_OVERSOLD_THRESHOLD = 30
TRADE_QUANTITY = 0.000001
LIMIT=200

# Coindcx API endpoints
PRICE_ENDPOINT = 'https://public.coindcx.com/market_data/trade_history'
ORDER_ENDPOINT = 'https://api.coindcx.com/exchange/v1/orders/create_market_order'

def fetch_data():
    params = {'pair': PAIR, 'limit': LIMIT}
    response = requests.get(PRICE_ENDPOINT, params=params)
    data = json.loads(response.text)

    # Creating pandas dataframe
    df = pd.DataFrame(data)
    
    df.fillna(method='ffill', inplace=True)

    # Extracting closing price data
    #close_data = df['p'].astype(float).to_numpy()
    #close_data = np.reshape(close_data, (-1, 1))
    close_data = np.array([float(entry['p']) for entry in data])
    close_data = close_data.reshape(-1, 1)

    # Calculating RSI data
    rsi_data = RSI(close_data.ravel(), WINDOW_SIZE)
    rsi_data = np.nan_to_num(rsi_data)


    # Combining close_data and rsi_data
    #combined_data = np.concatenate((close_data, rsi_data.reshape(-1, 1)), axis=1)

    # Scaling data between 0 and 1
    #scaler = MinMaxScaler(feature_range=(0, 1))
    #scaled_data = np.nan_to_num(scaler.fit_transform(combined_data))

    # Splitting the scaled data back into close_data and rsi_data
    #close_data = scaled_data[:, 0].reshape(-1, 1)
    #rsi_data = scaled_data[:, 1].reshape(-1, 1)
    
    # Trimming rsi_data to match the number of samples in close_data
    rsi_data = rsi_data[-len(close_data):]

    # Scaling data between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_close_data = np.nan_to_num(scaler.fit_transform(close_data))
    scaled_rsi_data = np.nan_to_num(scaler.fit_transform(rsi_data.reshape(-1, 1)))

    return scaled_close_data, scaled_rsi_data, scaler

# Visualizing the data
def visualize_data(close_data, predicted_prices):
    plt.figure(figsize=(12, 6))
    plt.plot(close_data, label='Actual Prices')
    plt.plot(predicted_prices, label='Predicted Prices')
    plt.title('Actual Prices vs. Predicted Prices')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

def place_order(pair, side, quantity):
    # Implement your code here to place the order based on the provided pair, side, and quantity
    # This function will vary depending on the trading platform or API you are using
    # Make sure to handle any necessary authentication or authorization steps

    # Example code for placing an order using a hypothetical trading API
    # Replace this code with your own implementation

    if side == 'buy':
        print(f"Placing a buy order for {quantity} {pair}")
    elif side == 'sell':
        print(f"Placing a sell order for {quantity} {pair}")
    else:
        print("Invalid order side. Please provide 'buy' or 'sell'.")

    return

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
        X_train.append(np.concatenate((train_data[i - 60:i, 0], rsi_train_data[i - 60:i, 0]), axis=0))
        y_train.append(train_data[i, 0])

    # Converting training data to numpy arrays
    X_train, y_train = np.array(X_train), np.array(y_train)

    print("X_train shape before reshaping:", X_train.shape)
    # Reshape X_train to have two dimensions
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Creating LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))

    # Compiling the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Training the model
    model.fit(X_train, y_train, epochs=1, batch_size=1)

    # Testing data
    test_data = close_data[training_data_len - 60:, :]
    rsi_test_data = rsi_data[training_data_len - 60:, :]
    X_test = []
    y_test = close_data[training_data_len:, :]
    for i in range(60, len(test_data)):
        X_test.append(np.concatenate((test_data[i - 60:i, 0], rsi_test_data[i - 60:i, 0]), axis=0))

    # Converting test data to numpy arrays
    X_test = np.array(X_test)

    # Reshaping the data
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Predicting prices using the model
    predicted_prices = model.predict(X_test)
    predicted_prices = np.concatenate((predicted_prices, np.zeros_like(predicted_prices)), axis=1)
    predicted_prices = scaler.inverse_transform(predicted_prices)[:, 0]


    # Visualize the data
    visualize_data(close_data[training_data_len:], predicted_prices)

    # Check if there are any NaN values in the data
    if np.isnan(close_data).any() or np.isnan(predicted_prices).any():
        print("Input data contains NaN values. Please handle missing data.")
        return

    # Preprocess data
    close_data = close_data[WINDOW_SIZE:]
    predicted_prices = predicted_prices[:-WINDOW_SIZE]
    
    # Check if there are enough data points for RSI calculation
    if len(close_data) < WINDOW_SIZE:
        print("Insufficient data points for RSI calculation.")
        return

    # Trading strategy
    last_price = close_data[-1]
    predicted_price = predicted_prices[-1]
    rsi = RSI(np.append(close_data, predicted_prices))

    # Check breakout condition
    if predicted_price > last_price * BREAKOUT_THRESHOLD and rsi[-1] > RSI_OVERBOUGHT_THRESHOLD:
        # Place a sell order
        place_order(PAIR, 'sell', TRADE_QUANTITY)
    elif predicted_price < last_price / BREAKOUT_THRESHOLD and rsi[-1] < RSI_OVERSOLD_THRESHOLD:
        # Place a buy order
        place_order(PAIR, 'buy', TRADE_QUANTITY)
    else:
        print("No trading opportunity.")

    return predicted_prices, y_test


# Evaluation
from sklearn.metrics import classification_report, confusion_matrix

# Converting predictions to class labels
threshold = 0.5  # Adjust the threshold as per requirements
predicted_prices, y_test = trade()
predicted_labels = predicted_prices
actual_labels = y_test

from sklearn.metrics import accuracy_score

# Assuming you have actual_labels and predicted_labels variables

accuracy = accuracy_score(actual_labels, predicted_labels)
print("Accuracy score:", accuracy)


# Classification report
report = classification_report(actual_labels, predicted_labels)
print("Classification Report:")
print(report)

# Confusion matrix
cm = confusion_matrix(actual_labels, predicted_labels)
print("Confusion Matrix:")
print(cm)