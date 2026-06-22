#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Libraries
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential
import yfinance as yf


# In[2]:


CRYPTO_CURRENCY = 'BTC'
AGAINST_CURRENCY = 'INR'
START = dt.datetime(2023,5,1)
END = dt.datetime.now()
PERIOD = '1d'
INERVAL = "5m"


# In[3]:


# Read Data
data = yf.download(f"{CRYPTO_CURRENCY}-{AGAINST_CURRENCY}", start=START, end=END, period=PERIOD, interval=INERVAL)
#! pip install pycryptodome pycryptodomex
#! pip uninstall --yes pandas-datareader
#! pip install git+https://github.com/raphi6/pandas-datareader.git@ea66d6b981554f9d0262038aef2106dda7138316


# In[4]:


# Data Prepration and Analysis
data.tail()


# In[5]:


scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))
# prediction_days = 60 # for 1 day interval prediction
prediction_days = 288  # 1 day period with 5-minute interval (24 hours * 60 minutes / 5 minutes)
# future day = 30 # to predict for next 30th day
x_train, y_train = [], []
for x in range(prediction_days, len(scaled_data)): # for future days -> len(scaled_data) - future day
    x_train.append(scaled_data[x-prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))


# In[ ]:


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


# In[ ]:


# test model
test_data = yf.download("BTC-INR", start=START, end=END)
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

plt.plot(actual_prices, color='black', label='Actual Prices')
plt.plot(prediction_prices, color='green', label='Predicted Prices')
plt.title(f"{CRYPTO_CURRENCY} Price Prediction")
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.show()


# In[ ]:


# Predict Next Day
real_data = [model_inputs[len(model_inputs)+1 - prediction_days: len(model_inputs) + 1, 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)
print(prediction)


# In[ ]:


from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
r2 = r2_score(actual_prices, prediction_prices)
r2


# In[ ]:




