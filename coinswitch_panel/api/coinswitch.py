import requests

BASE_URL = "https://exchange.coinswitch.co"

def broker_balance(headers,body):
    return requests.get(f"{BASE_URL}/api/v2/me/balance/", headers=headers)

def master_balance(headers,body):
    return requests.get(f"{BASE_URL}/api/v1/master/me/getBalance/", headers=headers)

def cancel_order(headers,body):
    return requests.delete(f"{BASE_URL}/api/v1/orders/{body}", headers=headers)

def cancel_all_order(headers,body):
    return requests.delete(f"{BASE_URL}/api/v1/orders/cancelAll?instrument=USDT/INR", headers=headers)

def recent_orders(headers,body):
    return requests.get(f"{BASE_URL}/api/v1/me/orders/?onlyOpen=false&type=LIMIT", headers=headers)

def buy_market_order(headers,body):
    return requests.post(f"{BASE_URL}/api/v1/orders/",json=body, headers=headers)

def buy_limit_order(headers,body):
    return requests.post(f"{BASE_URL}/api/v1/orders/",json=body, headers=headers)

def transfer_master_to_broker(headers,body):
    return requests.post(f"{BASE_URL}/api/v1/master/me/transferFunds",json=body, headers=headers)

def crypto_withdrawal(headers,body):
    return requests.post(f"{BASE_URL}/api/v1/me/withdrawal",json=body, headers=headers)

def transfer_broker_to_master(headers,body):
    return requests.post(f"{BASE_URL}/api/v1/master/me/transferFunds",json=body, headers=headers)

def inr_withdrawal(headers,body):
    return requests.post(f"{BASE_URL}/api/v1/me/inrWithdrawal",json=body, headers=headers)

def sell_market_order(headers,body):
    return requests.post(f"{BASE_URL}/api/v1/orders/",json=body, headers=headers)

def sell_limit_order(headers,body):
    return requests.post(f"{BASE_URL}/api/v1/orders/",json=body, headers=headers)















# def transfer_broker_to_master(headers,data):
#     return requests.post(f"{BASE_URL}/api/v1/master/me/transferFunds",json=data, headers=headers)
