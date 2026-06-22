import pandas as pd
import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# from keras.models import Sequential
# from keras.layers import Dense
from upstox_api.api import Upstox

# Replace with your API key and secret key
api_key = 'a76e7550-c54c-4035-8924-141fc0c99cdb'
api_secret = 'gh150tlrhp'
upstox = Upstox('gh150tlrhp', 'a76e7550-c54c-4035-8924-141fc0c99cdb')
# Create an Upstox API instance
# u = upstox.Upstox(api_key, api_secret)

# # Login to the API
# login_url = u.get_login_url()
# print('Please visit this URL to authorize the API:', login_url)

# # Once you authorize the API, enter the authorization code
# access_token = u.get_access_token('your_authorization_code')
# u.set_access_token(access_token)

# retrieve data
start_date = '2022-01-01'
end_date = '2022-03-30'
symbol = 'SBIN'
interval = 'day'
data = upstox.get_historical_data(
    exchange='NSE_EQ',
    symbol=symbol,
    start_date=start_date,
    end_date=end_date,
    interval=interval
)
df = pd.DataFrame(data)
df = df[['timestamp', 'close']]
df = df.rename(columns={'timestamp': 'Date', 'close': 'Close'})
df = df.reset_index(drop=True)

print(df)