from flask_restful import Resource
from flask import Flask, request, jsonify
from models.Trades import Trades
import requests
from lib.db import db
from sqlalchemy import asc, desc
import numpy as np
import pandas as pd
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential
import yfinance as yf
import talib
import time


CRYPTO_CURRENCY = 'BTC'
AGAINST_CURRENCY = 'INR'
SYMBOL = "BTC-INR"
END = dt.datetime.now()
START = pd.to_datetime(END) - pd.DateOffset(days=2)
PERIOD = '1d'
INTERVAL = "5m"
RSI_UPPER_LIMIT = 70
RSI_LOWER_LIMIT = 30

class PredictionModel(Resource):
    def get(self):
        print("Hello")
        global SYMBOL
        tradesQuery = Trades.query.with_entities(Trades.id, Trades.symbol, Trades.position, Trades.amount, Trades.status, Trades.createdAt, Trades.userId, Trades.profitLimit, Trades.stopLoss).filter_by(status=0).order_by(asc(Trades.id)).first()
        if tradesQuery:
            tradesQuery = tradesQuery._asdict()
            profit_limit = tradesQuery["profitLimit"]  # Desired profit limit (in percentage)
            stop_loss = tradesQuery["stopLoss"]   # Desired stop loss (in percentage)
            SYMBOL = tradesQuery["symbol"][0:3]+"-"+tradesQuery["symbol"][3:]
            Trades.query.filter(Trades.id == tradesQuery['id']).update({Trades.status: 1})
            db.session.commit()
            print("Inside if")
            while True:
                # Read Data
                data = yf.download(SYMBOL, start=START, end=END, period=PERIOD, interval=INTERVAL)
                scaler = MinMaxScaler(feature_range=(0, 1))
                scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
                prediction_days = 288  # 1 day period with 5-minute interval (24 hours * 60 minutes / 5 minutes)

                x_train, y_train = [], []
                for x in range(prediction_days, len(scaled_data)):
                    x_train.append(scaled_data[x - prediction_days:x, 0])
                    y_train.append(scaled_data[x, 0])

                x_train, y_train = np.array(x_train), np.array(y_train)
                x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

                # Create Neural Network
                model = Sequential()
                model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
                model.add(Dropout(0.2))
                model.add(LSTM(units=50, return_sequences=True))
                model.add(Dropout(0.2))
                model.add(LSTM(units=50))
                model.add(Dropout(0.2))
                model.add(Dense(units=1))

                model.compile(optimizer='adam', loss='mean_squared_error')
                model.fit(x_train, y_train, epochs=25, batch_size=32)

                # test model
                test_data = yf.download(SYMBOL, start=START, end=END, period=PERIOD, interval=INTERVAL)
                actual_prices = test_data['Close'].values
                total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

                model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
                model_inputs = model_inputs.reshape(-1, 1)
                model_inputs = scaler.fit_transform(model_inputs)

                x_test = []
                for x in range(prediction_days, len(model_inputs)):
                    x_test.append(model_inputs[x-prediction_days:x, 0])

                x_test = np.array(x_test)
                x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

                prediction_prices = model.predict(x_test)
                prediction_prices = scaler.inverse_transform(prediction_prices)

                prediction_prices = model.predict(x_test)
                prediction_prices = scaler.inverse_transform(prediction_prices)

                # Predict Next Day
                real_data = [model_inputs[len(model_inputs)+1 - prediction_days: len(model_inputs) + 1, 0]]
                real_data = np.array(real_data)
                real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

                prediction = model.predict(real_data)
                prediction = scaler.inverse_transform(prediction)
                print(prediction)

                # Get the last predicted price and the previous actual price
                last_predicted_price = prediction_prices[-1]
                previous_actual_price = actual_prices[-2]
                latest_actual_price = actual_prices[-1]

                # Calculate the current profit/loss percentage
                current_profit = ((latest_actual_price - previous_actual_price) / previous_actual_price) * 100

                # Determine the market direction
                if last_predicted_price < previous_actual_price and talib.RSI(actual_prices) > RSI_UPPER_LIMIT:
                    market_direction = "Market is likely to go down. Place SELL Order!!"
                    print(market_direction)
                    break
                elif last_predicted_price > previous_actual_price and talib.RSI(actual_prices) < RSI_LOWER_LIMIT:
                    market_direction = "Market is likely to go up. Place BUY Order!!"
                    print(market_direction)
                    break
                elif current_profit >= profit_limit:
                    print("Profit limit achieved. Exiting program.")
                    break
                elif current_profit <= -stop_loss:
                    print("Stop loss achieved. Exiting program.")
                    break
                else:
                    market_direction = "Market is likely to remain unchanged."
                    print(market_direction)
                
                print(f"Current Profit/Loss: {current_profit:.2f}%")
                Trades.query.filter(Trades.id == tradesQuery['id']).update({Trades.position: current_profit})
                db.session.commit()

                # # Check if profit limit or stop loss is achieved
                # if current_profit >= profit_limit:
                #     print("Profit limit achieved. Exiting program.")
                #     break
                # elif current_profit <= -stop_loss:
                #     print("Stop loss achieved. Exiting program.")
                #     break
                
                time.sleep(5)

            Trades.query.filter(Trades.id == tradesQuery['id']).update({Trades.status: 2})
            db.session.commit()
            return jsonify({'market_direction': market_direction})
        else:
            return jsonify({'market_direction': 'No trades to execute'})