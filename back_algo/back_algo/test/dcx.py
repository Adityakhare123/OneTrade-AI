import requests # Install requests module first.

url = "https://api.coindcx.com/exchange/ticker"

response = requests.get(url)
data = response.json()
print(data[:4])

api_key = "c4b8d9739639e97a054a212164f4ded54d5d9dfa9cfee950"
api_secrate = "ab27218910bc0ec403148648ae417e3dddc2b6fec00dd6343eeaaa7b8e7ac682"