import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import requests # Install requests module first.

# Load data
################## Realtime Data #######################
# url = "https://api.coindcx.com/exchange/ticker"

# response = requests.get(url)
# data = response.json()
########################################################

################## Sample Data #########################
data = [{'market': 'BTCINR', 'change_24_hour': '1.791', 'high': '2500000.0', 'low': '2450000.02', 'volume': '4869455.877066289', 'last_price': '2493998.990000000000', 'bid': '2458939.620000000000', 'ask': '2493998.990000000000', 'timestamp': 1680331490}]
########################################################
data = pd.DataFrame(data)
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Check for non-numeric values in X
X.apply(pd.to_numeric, errors='coerce').isnull().any()

# Encode categorical columns
from sklearn.preprocessing import LabelEncoder
encoders = {}
for col in X.select_dtypes(include=['object']).columns:
    encoders[col] = LabelEncoder()
    X[col] = encoders[col].fit_transform(X[col])

# Create model
model = Sequential()
model.add(Dense(10, input_dim=X.shape[1], activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
model.fit(X, y, epochs=100)

# Make predictions
predictions = model.predict(X)
print("predictions: ", predictions)