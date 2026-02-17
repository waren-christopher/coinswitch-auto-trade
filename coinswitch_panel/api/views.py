from django.shortcuts import render
from . import coinswitch,signature_server
import os,time
from dotenv import load_dotenv
from django.http import JsonResponse


load_dotenv()

def dashboard(request):
    #for render html,css,js when refresh or access the site via browser
    if request.method == "GET":
        return render(request, "dashboard.html")

    #get datas for generat signature from html 
    if request.method == "POST":
        api_action = request.POST.get('api')
        api,method,url_path,publickey,secretkey=api_action.split("+")
        
    timestamp = str(int(time.time()))

    
    try:
       body = {k: v for k, v in request.POST.items() if k not in ('api', 'csrfmiddlewaretoken','secretkey','publickey')}
       map = {'fromID': 'masterid' if api == 'transfer_master_to_broker' else 'brokerid',
              'toID': 'brokerid' if api == 'transfer_master_to_broker' else 'masterid',
              'address': 'ledger_address', }
       #get values from .env file
       for body_key, env_key in map.items():
           if body_key in body:
               body[body_key] = os.getenv(env_key)
       if api == 'cancel_order':
           url_path ,orderid=url_path + body['orderId'], body['orderId']   #merge urlpath and order id to pass cancel order function 
           body={}
       if api == 'crypto_withdrawal':
           body['amount'] = float(body['amount']) if '.' in body['amount'] else int(body['amount']) #handle integer and fload values 
       if api == 'buy_market_order' or api == 'buy_limit_order' or api == 'sell_limit_order':  #calculate trading fee of 0.15%
           fee=float(round(float(body['quantity']) * 0.0015, 2)) if '.' in body['quantity'] else int(int(body['quantity']) * 0.0015)
           body['quantity']=str(float(body['quantity']) - fee if '.' in body['quantity'] else int(body['quantity']) - fee)
           api == 'buy_market_order' and body.update({'bestQuantity': body['quantity']})
 
    except Exception as e:
        print(str(e))
        body = {}

    payload = {
        "method": method,
        "urlPath": url_path,
        "message": body,
        "timestamp": timestamp,
    }
    # print('payload is: ',payload,os.getenv('secretkey'))
    # return
    signature = signature_server.django_generate_signatures(os.getenv(secretkey), payload)

    headers = {
    "Content-Type": "application/json",
    "connection" : "keep-alive",
    "Accept": "application/json",
    "CSX-ACCESS-KEY" : os.getenv(publickey),  
    "CSX-SIGNATURE" : signature,
    "CSX-ACCESS-TIMESTAMP" : timestamp,
     }
  #  return
    body=orderid if api == 'cancel_order' else body        #for send order id to function
    response=getattr(coinswitch, api)(headers,body) 
    

    try:
        data=response.json()
        if api == 'crypto_withdrawal' or api == 'inr_withdrawal':
            with open('request.txt', 'a', encoding='utf-8') as file:
               file.write(f"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {response.text}\n")
    except Exception:
        data=response.text

    return JsonResponse({"data":data ,"status":response.status_code})


