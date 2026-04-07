# import requests

# BASE_URL = "https://exchange.coinswitch.co"

# def broker_balance(headers,body):
#     return requests.get(f"{BASE_URL}/api/v2/me/balance/", headers=headers)

# def master_balance(headers,body):
#     return requests.get(f"{BASE_URL}/api/v1/master/me/getBalance/", headers=headers)

# def cancel_order(headers,body):
#     return requests.delete(f"{BASE_URL}/api/v1/orders/{body}", headers=headers)

# def cancel_all_order(headers,body):
#     return requests.delete(f"{BASE_URL}/api/v1/orders/cancelAll?instrument=USDT/INR", headers=headers)

# def recent_orders(headers,body):
#     return requests.get(f"{BASE_URL}/api/v1/me/orders/?onlyOpen=false&type=LIMIT", headers=headers)

# def buy_market_order(headers,body):
#     return requests.post(f"{BASE_URL}/api/v1/orders/",json=body, headers=headers)

# def buy_limit_order(headers,body):
#     return requests.post(f"{BASE_URL}/api/v1/orders/",json=body, headers=headers)

# def transfer_master_to_broker(headers,body):
#     return requests.post(f"{BASE_URL}/api/v1/master/me/transferFunds",json=body, headers=headers)

# def crypto_withdrawal(headers,body):
#     return requests.post(f"{BASE_URL}/api/v1/me/withdrawal",json=body, headers=headers)

# def transfer_broker_to_master(headers,body):
#     return requests.post(f"{BASE_URL}/api/v1/master/me/transferFunds",json=body, headers=headers)

# def inr_withdrawal(headers,body):
#     return requests.post(f"{BASE_URL}/api/v1/me/inrWithdrawal",json=body, headers=headers)

# def sell_market_order(headers,body):
#     return requests.post(f"{BASE_URL}/api/v1/orders/",json=body, headers=headers)

# def sell_limit_order(headers,body):
#     return requests.post(f"{BASE_URL}/api/v1/orders/",json=body, headers=headers)


import os
import time
import requests
from . import signature_server 

BASE_URL = "https://exchange.coinswitch.co"

def _generate_headers(method, url_path, body, pub_key_env, sec_key_env):
    """Internal helper to generate secure headers for CoinSwitch"""
    timestamp = str(int(time.time()))
    payload = {
        "method": method,
        "urlPath": url_path,
        "message": body,
        "timestamp": timestamp,
    }
    
    public_key = os.getenv(pub_key_env)
    secret_key = os.getenv(sec_key_env)
    
    signature = signature_server.django_generate_signatures(secret_key, payload)

    return {
        "Content-Type": "application/json",
        "connection": "keep-alive",
        "Accept": "application/json",
        "CSX-ACCESS-KEY": public_key,
        "CSX-SIGNATURE": signature,
        "CSX-ACCESS-TIMESTAMP": timestamp,
    }

# --- THE 13 COINSWITCH FUNCTIONS ---

def broker_balance(body):
    url_path = "/api/v2/me/balance/"
    headers = _generate_headers("GET", url_path, {}, "publickey", "secretkey")
    return requests.get(f"{BASE_URL}{url_path}", headers=headers)

def master_balance(body):
    url_path = "/api/v1/master/me/getBalance/"
    headers = _generate_headers("GET", url_path, {}, "master_publickey", "master_privatekey")
    return requests.get(f"{BASE_URL}{url_path}", headers=headers)

def cancel_order(body):
    order_id = body.get('orderId', '')
    url_path = f"/api/v1/orders/{order_id}"
    headers = _generate_headers("DELETE", url_path, {}, "publickey", "secretkey")
    return requests.delete(f"{BASE_URL}{url_path}", headers=headers)

def cancel_all_order(body):
    url_path = "/api/v1/orders/cancelAll?instrument=USDT/INR"
    headers = _generate_headers("DELETE", url_path, {}, "publickey", "secretkey")
    return requests.delete(f"{BASE_URL}{url_path}", headers=headers)

def recent_orders(body):
    url_path = "/api/v1/me/orders/?onlyOpen=false&type=LIMIT"
    headers = _generate_headers("GET", url_path, {}, "publickey", "secretkey")
    return requests.get(f"{BASE_URL}{url_path}", headers=headers)

def particular_order_details(order_id):
    url_path = f"/api/v1/orders/{order_id}"
    headers = _generate_headers("GET", url_path, {}, "publickey", "secretkey")
    return requests.get(f"{BASE_URL}{url_path}", headers=headers)

def buy_market_order(body):
    fee=float(round(float(body['quantity']) * 0.0015, 2)) if '.' in body['quantity'] else int(int(body['quantity']) * 0.0015)
    body['quantity']=str(float(body['quantity']) - fee if '.' in body['quantity'] else int(body['quantity']) - fee)
    body['bestQuantity'] = body['quantity']
    url_path = "/api/v1/orders/"
    print('ksdjfkslf',body)
    headers = _generate_headers("POST", url_path, body, "publickey", "secretkey")
    return requests.post(f"{BASE_URL}{url_path}", json=body, headers=headers)

def buy_limit_order(body):
    body=body.copy()
    print('copied body ',body)
    fee=float(round(float(body['quantity']) * 0.0015, 2)) if '.' in body['quantity'] else int(int(body['quantity']) * 0.0015)
    quantity=float(body['quantity']) - fee if '.' in body['quantity'] else int(body['quantity']) - fee
    body['quantity']=str(round(quantity, 2))
    url_path = "/api/v1/orders/"
    headers = _generate_headers("POST", url_path, body, "publickey", "secretkey")
    return requests.post(f"{BASE_URL}{url_path}", json=body, headers=headers)

def sell_limit_order(body):
    body=body.copy()
    fee = float(round(float(body['quantity']) * 0.0015, 2)) if '.' in body['quantity'] else int(int(body['quantity']) * 0.0015)
    quantity = float(body['quantity']) - fee if '.' in body['quantity'] else int(body['quantity']) - fee
    body['quantity']=str(round(quantity, 2))
    url_path = "/api/v1/orders/"
    headers = _generate_headers("POST", url_path, body, "publickey", "secretkey")
    return requests.post(f"{BASE_URL}{url_path}", json=body, headers=headers)

def transfer_master_to_broker(body):
    body['fromID'] = os.getenv('masterid')
    body['toID'] = os.getenv('brokerid')
    url_path = "/api/v1/master/me/transferFunds"
    headers = _generate_headers("POST", url_path, body, "master_publickey", "master_privatekey")
    return requests.post(f"{BASE_URL}{url_path}", json=body, headers=headers)

def crypto_withdrawal(body):
    body['amount'] = float(body['amount']) if '.' in body['amount'] else int(body['amount'])
    if 'address' not in body:
        body['address'] = os.getenv('ledger_address')
    url_path = "/api/v1/me/withdrawal"
    headers = _generate_headers("POST", url_path, body, "master_publickey", "master_privatekey")
    response = requests.post(f"{BASE_URL}{url_path}", json=body, headers=headers)
    
    with open('request.txt', 'a', encoding='utf-8') as file:
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} {response.text}\n")
    return response

def transfer_broker_to_master(body):
    body['fromID'] = os.getenv('brokerid')
    body['toID'] = os.getenv('masterid')
    url_path = "/api/v1/master/me/transferFunds"
    headers = _generate_headers("POST", url_path, body, "master_publickey", "master_privatekey")
    return requests.post(f"{BASE_URL}{url_path}", json=body, headers=headers)

def inr_withdrawal(body):
    url_path = "/api/v1/me/inrWithdrawal"
    headers = _generate_headers("POST", url_path, body, "master_publickey", "master_privatekey")
    response = requests.post(f"{BASE_URL}{url_path}", json=body, headers=headers)
    
    with open('request.txt', 'a', encoding='utf-8') as file:
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} {response.text}\n")
    return response

