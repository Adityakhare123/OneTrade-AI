
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from upstox_api.api import Upstox

# Replace with your API key and secret key
# api_key = 'a76e7550-c54c-4035-8924-141fc0c99cdb'
# api_secret = 'gh150tlrhp'
# upstox = Upstox('a76e7550-c54c-4035-8924-141fc0c99cdb', 'gh150tlrhp')
# Create an Upstox API instance
# u = upstox.Upstox(api_key, api_secret)

# # Login to the API
# login_url = u.get_login_url()
# print('Please visit this URL to authorize the API:', login_url)

# # Once you authorize the API, enter the authorization code
# access_token = u.get_access_token('your_authorization_code')
# u.set_access_token(access_token)

# retrieve data
# start_date = '2022-01-01'
# end_date = '2022-03-30'
# symbol = 'SBIN'
# interval = 'day'
# data = upstox.get_historical_data(
#     exchange='NSE_EQ',
#     symbol=symbol,
#     start_date=start_date,
#     end_date=end_date,
#     interval=interval
# )
import requests # Install requests module first.

url = "https://api.coindcx.com/exchange/ticker"

response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)
df = df[['timestamp', 'close']]
df = df.rename(columns={'timestamp': 'Date', 'close': 'Close'})
df = df.reset_index(drop=True)



# # load data
# df = pd.read_csv('TATASTEEL.csv')
# df = df[['Date', 'Close']]
# df = df[::-1]
# df = df.reset_index(drop=True)

# normalize data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

# split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(scaled_data[:-60], scaled_data[60:], test_size=0.2, shuffle=False)

# create ANN model
model = Sequential()
model.add(Dense(units=32, input_dim=60, activation='relu'))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=1, activation='linear'))

# compile model
model.compile(optimizer='adam', loss='mean_squared_error')

# train model
model.fit(X_train[:, :-1], y_train, epochs=50, batch_size=32)

# make predictions
x_test = X_test[:-60, :-1]
y_test = y_test[60:]
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# plot results
import matplotlib.pyplot as plt

plt.plot(df['Close'][len(X_train)+60:].values)
plt.plot(predictions)
plt.show()
