import requests
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Step 1: Collect and preprocess data
response = requests.get('https://api.coindcx.com/exchange/ticker')
data = response.json()
print(data)
# Loop through the list of dictionaries until you find the 'BTC-INR' pair
btc_inr_price = None
for pair_data in data:
    if pair_data['market'] == 'BTCINR':
        btc_inr_price = pair_data['last_price']
        break

# TODO: implement data collection and preprocessing code
# Placeholder code for generating training and test data
input_dim = 3
X_train = np.random.rand(100, input_dim)
y_train = np.random.rand(100, 1)
X_test = np.random.rand(20, input_dim)
y_test = np.random.rand(20, 1)

# Step 2: Define your ANN architecture
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(input_dim,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='linear')
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Step 3: Train your ANN
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Step 4: Test your ANN
test_loss = model.evaluate(X_test, y_test)

# Step 5: Develop a trading strategy based on the ANN predictions
predictions = model.predict(X_test)
# TODO: implement trading strategy based on predictions

print("Current Bitcoin price in INR:", btc_inr_price)