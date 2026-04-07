import requests
BASE_URL = "https://exchange.coinswitch.co"

def buy_limit_order():
    return requests.get(f"https://exchange.coinswitch.co/api/v2/public/depth/?instrument=usdt/inr")

data=buy_limit_order()
print(data.json())
