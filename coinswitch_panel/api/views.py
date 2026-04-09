from django.shortcuts import render,redirect
from . import coinswitch,signature_server
import os,time,threading,requests
from dotenv import load_dotenv
from django.http import JsonResponse
from django.core.mail import send_mail
import random

load_dotenv()

# def forgot_password(request):
#     context = {}

#     if request.method == "POST":
#         action = request.POST.get("action")
#         username = request.POST.get("username")

#         context["username"] = username

#         # STEP 1 → SHOW CONFIRMATION
#         if action == "check_user":
#             try:
#                 user = User.objects.get(username=username)
#                 context["show_confirm"] = True
#             except User.DoesNotExist:
#                 context["error"] = "User not found"

#         # STEP 2 → SEND OTP
#         elif action == "send_otp":
#  # otp = random.randint(100000, 999999)     
#       # send_mail(
#       # 'Your OTP Code',
#       # f'''Hello dear user👋,
      
#       # Your One-Time Password (OTP) is:
      
#       # 👉 {otp}
      
#       # ⏳ This OTP is valid for 5 minutes.
#       # ❗ Do not share this OTP with anyone.
      
#       # If you didn’t request this, please ignore this email.
      
#       # Thanks,
#       # Your App Team 🚀''',
#       # 'warenchrist767@gmail.com',
#       # ['warenchrist00@gmail.com'],
#       # fail_silently=False,
#       #  )
#       # print('orp send succesfully ',otp)
#             context["show_otp"] = True

#         # STEP 3 → VERIFY OTP
#         elif action == "verify_otp":
#             entered_otp = request.POST.get("otp")

#             if entered_otp == request.session.get("otp"):
#                 context["show_password"] = True
#             else:
#                 context["error"] = "Invalid OTP"
#                 context["show_otp"] = True

#         # STEP 4 → RESET PASSWORD
#         elif action == "reset_password":
#             password = request.POST.get("password")
#             username = request.session.get("username")

#             user = User.objects.get(username=username)
#             user.set_password(password)
#             user.save()

#             return redirect("login")

#     return render(request, "forgot_password.html", context)

# def auto_trade(request):
#     print(request.POST)
#     return JsonResponse({
#             "final_price": round(255, 2),
#             "side": 'sjfksjf'
#         })
    
#     if request.method == "POST":
#         price_range = request.POST.get("price_range")
#         min_qty = float(request.POST.get("min_qty"))
#         quantity = request.POST.get("quantity")
#         side = request.POST.get("side")

#         min_price, max_price = map(float, price_range.split("-"))

#         data = get_orderbook()  # your function
#         best = data["data"]["sell"][0] if side == "BUY" else data["data"]["buy"][0]

#         price = float(best[0])
#         qty = float(best[1])

#         if qty >= min_qty:
#             price += 0.01

#         if price > max_price:
#             return JsonResponse({"msg": "Max price reached"})

#         return JsonResponse({
#             "final_price": round(price, 2),
#             "side": side
#         })
    
    
# def auto_trade_page(request):
#     return render(request, "auto_trade.html")






# def dashboard(request):
#     #for render html,css,js when refresh or access the site via browser
#     if not request.session.get('user'):
#         return redirect('login')
#     if request.method == "GET":
#         return render(request, "dashboard.html")
        

#     #get datas for generat signature from html 
#     if request.method == "POST":
#         api_action = request.POST.get('api')
#         api,method,url_path,publickey,secretkey=api_action.split("+")
        
#     timestamp = str(int(time.time()))

    
#     try:
#        body = {k: v for k, v in request.POST.items() if k not in ('api', 'csrfmiddlewaretoken','secretkey','publickey')}
#        map = {'fromID': 'masterid' if api == 'transfer_master_to_broker' else 'brokerid',
#               'toID': 'brokerid' if api == 'transfer_master_to_broker' else 'masterid',
#               'address': 'ledger_address', }
#        #get values from .env file
#        for body_key, env_key in map.items():
#            if body_key in body:
#                body[body_key] = os.getenv(env_key)
#        if api == 'cancel_order':
#            url_path ,orderid=url_path + body['orderId'], body['orderId']   #merge urlpath and order id to pass cancel order function 
#            body={}
#        if api == 'crypto_withdrawal':
#            body['amount'] = float(body['amount']) if '.' in body['amount'] else int(body['amount']) #handle integer and fload values 
#        if api == 'buy_market_order' or api == 'buy_limit_order' or api == 'sell_limit_order':  #calculate trading fee of 0.15%
#            fee=float(round(float(body['quantity']) * 0.0015, 2)) if '.' in body['quantity'] else int(int(body['quantity']) * 0.0015)
#            body['quantity']=str(float(body['quantity']) - fee if '.' in body['quantity'] else int(body['quantity']) - fee)
#            api == 'buy_market_order' and body.update({'bestQuantity': body['quantity']})
 
#     except Exception as e:
#         print(str(e))
#         body = {}

#     payload = {
#         "method": method,
#         "urlPath": url_path,
#         "message": body,
#         "timestamp": timestamp,
#     }
#     # print('payload is: ',payload,os.getenv('secretkey'))
#     # return
#     signature = signature_server.django_generate_signatures(os.getenv(secretkey), payload)

#     headers = {
#     "Content-Type": "application/json",
#     "connection" : "keep-alive",
#     "Accept": "application/json",
#     "CSX-ACCESS-KEY" : os.getenv(publickey),  
#     "CSX-SIGNATURE" : signature,
#     "CSX-ACCESS-TIMESTAMP" : timestamp,
#      }
#   #  return
#     body=orderid if api == 'cancel_order' else body        #for send order id to function
#     response=getattr(coinswitch, api)(headers,body) 
    

#     try:
#         data=response.json()
#        # print('ksdjfsjf',data)
#         if api == 'crypto_withdrawal' or api == 'inr_withdrawal':
#             with open('request.txt', 'a', encoding='utf-8') as file:
#                file.write(f"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} {response.text}\n")
#     except Exception:
#         data=response.text
#     return JsonResponse({"data":data ,"status":response.status_code})



# import pandas as pd
# from datetime import datetime, timezone, timedelta

def analyze_bot_performance(api_json_response, export_filename="coinswitch_trade_history.xlsx"):
    orders = api_json_response.get('data', {}).get('data', [])
    
    # Trackers for your Django dashboard
    total_trades = 0
    total_usdt_bought = 0.0
    total_inr_spent = 0.0
    
    # 1. Define IST Timezone (UTC + 5 hours 30 mins)
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    
    # 2. List to hold the extracted data for our Excel rows
    excel_rows = []
    
    for order in orders:
        filled_qty = float(order.get('filledQuantity', 0))
        filled_inr = float(order.get('filledQuoteQuantity', 0))
        
        # Update Dashboard Stats (Only count actual executions)
        if filled_qty > 0:
            total_trades += 1
            total_usdt_bought += filled_qty
            total_inr_spent += filled_inr
            
        # 3. Convert Unix Timestamp to readable IST Date & Time
        try:
            ts = int(order.get('createdAt', 0))
            # Tell Python this is UTC, then convert it to IST
            dt_ist = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(ist_tz)
            # Format nicely (e.g., "2026-04-02 12:35:10 PM")
            formatted_time = dt_ist.strftime('%Y-%m-%d %I:%M:%S %p')
        except (ValueError, TypeError):
            formatted_time = "Unknown"

        # 4. Extract exactly the data points you requested for Excel
        excel_rows.append({
            "Created At (IST)": formatted_time,
            "Instrument": order.get('instrument', ''),
            "Side": order.get('side', ''),
            "Status": order.get('status', ''),
            "Limit Price (INR)": float(order.get('limitPrice', 0)),
            "Requested Qty": float(order.get('quantity', 0)),
            "Filled Qty": filled_qty,
            "Filled Quote (INR)": filled_inr,
            "Cancelled Qty": float(order.get('cancelledQuantity', 0))
        })
        
    # Calculate VWAP (True Average Price)
    avg_price = total_inr_spent / total_usdt_bought if total_usdt_bought > 0 else 0
    
    # --- 5. CREATE AND SAVE THE EXCEL FILE ---
    if excel_rows:
        # Convert our list of dictionaries into a Pandas DataFrame
        df = pd.DataFrame(excel_rows)
        
        # Export straight to a local Excel file without the annoying index numbers
        df.to_excel(export_filename, index=False)
        print(f"📊 Excel file saved successfully as: {export_filename}")
    else:
        print("⚠️ No orders found to export.")

    # Return the summary exactly as before
    return {
        "executed_trades": total_trades,
        "total_usdt": round(total_usdt_bought, 4),
        "total_inr": round(total_inr_spent, 2),
        "average_buy_price": round(avg_price, 4)
    }



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 🔥 Replace this with psycopg2 query
        if username == "admin" and password == "1234":
            request.session['user'] = username   # ✅ create session
            return redirect('dashboard')
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")
def auto_trade_page(request):
    return render(request, "auto_trade.html")


bot_running = False
bot_message = ""
current_order_id = None
trade_quantity = ""

def start_auto_trade(request):
    global bot_running,bot_message,current_order_id

    if request.method == "POST":
        price_range = request.POST.get("price_range")
        min_qty = float(request.POST.get("min_qty"))
        body = {k: v for k, v in request.POST.items() if k not in ('price_range', 'min_qty')}
        print(body)

        if bot_running:
            return JsonResponse({"msg": "Bot already running"})

        bot_running = True
        current_order_id = None

        thread = threading.Thread(
            target=auto_trade_bot,
            args=(price_range, min_qty, body)
        )
        thread.start()
       # data= auto_trade_bot(price_range,min_qty,body)

        return JsonResponse({"msg":'started' })


def stop_auto_trade(request):
    global bot_running,current_order_id
    if current_order_id:
       cancel=coinswitch.cancel_order({'orderId': current_order_id}).json()
    bot_running = False
    return JsonResponse({"msg": f"bot stopped and {cancel}" })


def auto_trade_status(request):
    global bot_running,bot_message
    return JsonResponse({"running": bot_running,"message": bot_message})


def buy_sell_decision(side,competitor_price,limit_threshold,order_id):
    global bot_message,current_order_id
    if side == 'buy':
        target_price = round(competitor_price + 0.01, 2)
        
        # Safety Check: Did the market push us above our maximum budget?
        if target_price > limit_threshold:
            bot_message = f"Stopped: Target {target_price} exceeded max limit of {limit_threshold}."
            print(f"🛑 {bot_message}")
            if order_id:
                coinswitch.cancel_order({'orderId': order_id})
                current_order_id = None
            return "price range reached"
        return target_price
    else: # sell
        target_price = round(competitor_price - 0.01, 2)
        
        # Safety Check: Did the market drop below our minimum acceptable sell price?
        if target_price < limit_threshold:
            bot_message = f"Stopped: Target {target_price} dropped below min limit of {limit_threshold}."
            print(f"🛑 {bot_message}")
            if order_id:
                coinswitch.cancel_order({'orderId': order_id})
                current_order_id = None
            return "price range reached"
        return target_price

def replace_order(cancel_body,body):
    global bot_running, bot_message,current_order_id,trade_quantity
    try:
        cancel_res = coinswitch.cancel_order(cancel_body)
        print('order response',cancel_res.json())
    
        # Reset states so the next loop tick places a brand new order at the new target
        order_det=coinswitch.particular_order_details(current_order_id).json()
        filled_quantity=float(order_det['data']['filledQuoteQuantity'])
        print('got file quantity',filled_quantity)
        balance=coinswitch.broker_balance(body).json()
        balance=float(balance['data']['Available']['inr'])
        print('getting broker balance ',balance)
        print('calculating quantity',float(body['quantity']) - filled_quantity)
        quant=float(body['quantity']) - filled_quantity 
        actual_affordable_quant = quant if balance >= quant else balance
        # 3. STEP 2: Is this final amount allowed by CoinSwitch?
        if 300 > quant and balance > float(trade_quantity):
          print('getting total quantity from trade_quntity ',trade_quantity)
          return trade_quantity
        elif actual_affordable_quant < 300:
            print("🛑 [STOP] Remaining amount or balance is below the 300 INR minimum. Stopping safely.")
            bot_running = False
            bot_message = "Trade successfully completed (or insufficient funds to continue)."
            return ""

        print("fixed quantity",actual_affordable_quant)   
        # 4. If we made it here, the math is 100% safe to send to the API!
        return str(round(actual_affordable_quant, 2))
    except requests.exceptions.ConnectionError as e:
            print(f"📡 [NETWORK] Connection dropped in replace_order. Will retry. Error: {str(e)}")
            time.sleep(15)
            return ""
    except Exception as e:
        print(f"💥 CRASH IN REPLACE BLOCK: {str(e)}") # <--- Now you will see the error!
        bot_running=False
        bot_message = f"error : {str(e)}"
        print(f"error : {str(e)}")
        return ""

def auto_trade_bot(price_range, min_qty, body):
    global bot_running, bot_message,current_order_id,trade_quantity
    current_placed_price = None
    side = body['side'].lower()  # 'buy' or 'sell'
    limit_threshold = float(price_range) # Max price to buy, or Min price to sell

    print(f"🚀 Bot initialized: Side={side.upper()}, Limit Threshold={limit_threshold}, Min Qty={min_qty}")

    while bot_running:
        try:
            print("Fetching orderbook...")
            res = requests.get("https://exchange.coinswitch.co/api/v2/public/depth/?instrument=usdt/inr")
            
            if res.status_code != 200:
                bot_message=f"Error fetching orderbook: {res.json()}"
                return
                
            data = res.json()
            levels = data["data"][side]

            # 1. Find the top COMPETITOR price (ignoring our own order)
            competitor_price = None
            for level in levels:
                price = float(level[0])
                qty = float(level[1])

                # CRITICAL: Do not compete with our own active order
                if current_placed_price is not None and price == current_placed_price:
                    continue

                # Ensure competitor has enough volume to matter
                if qty >= min_qty:
                    competitor_price = price
                    break 

            if competitor_price is None:
                print("No valid competitor levels found.")
                time.sleep(3)
                continue

            target_price=buy_sell_decision(side,competitor_price,limit_threshold,current_order_id)
            if target_price == "price range reached":
                time.sleep(7)
                continue
            # 2. Determine our target price (+0.01 for buy, -0.01 for sell)

            print(f"Competitor: {competitor_price} | Our Target: {target_price} | Currently Placed at: {current_placed_price}")

            # 3. State Machine: Place, Hold, or Cancel/Replace
            if current_order_id is None:
                # PLACE NEW ORDER
                body['limitPrice'] = str(target_price)
                trade_quantity = body['quantity']
                print(f"Placing initial {side} order at {target_price}...")
                
                response = coinswitch.buy_limit_order(body) if side == 'buy' else coinswitch.sell_limit_order(body)
                resp_data = response.json()
                
                # Check for success (Adjust the condition based on CoinSwitch API's exact success response)
                if response.status_code == 200:
                    current_order_id = resp_data['data']['orderId']    
                    current_placed_price = target_price
                    bot_message = f"Active order at {target_price}"
                    print(f"✅ Order Placed. ID: {current_order_id}")
                    time.sleep(3)
                    continue
                else:
                    bot_message = f"API Error: {resp_data}"
                    print(f"❌ {bot_message}")
                    bot_running = False
                    return
            else:
                    try:
                        order_det=coinswitch.particular_order_details(current_order_id).json()
                        if order_det['data']['status'] == 'FULFILLED': # or 100 > float(body['quantity']) - float(order_det['data']['filledQuoteQuantity']):
                            balance=coinswitch.broker_balance(body).json()
                            balance=float(balance['data']['Available']['inr'])
                            if 300 > balance:
                                bot_running = False
                                bot_message = "Auto Trade successfully completed" 
                                return
                            raw_quantity= float(float(trade_quantity) if balance > float(trade_quantity) else str(balance))
                            body['quantity'] = str(round(raw_quantity, 2))
                            latest_order_id = coinswitch.buy_limit_order(body).json() if side == 'buy' else coinswitch.sell_limit_order(body).json()
                            print('order fullfilled so placed a new order')
                        
                            current_order_id = latest_order_id['data']['orderId'] 
                            current_placed_price = body['limitPrice']
                            bot_message = "order fullfilled so placed a new order..."
                            print('sleeping')
                            time.sleep(3)
                            continue
                    except Exception as e:
                        print('erorroro',str(e))
                        bot_message = f"ererr {str(e)}"
                        bot_running = False
                        return

                

                # CHECK IF WE ARE STILL AT THE TOP
            if current_placed_price != target_price:
                print(f"Price moved! We are at {current_placed_price}, target is {target_price}. Canceling & Replacing...")
                try:
                    cancel_body = {'orderId': current_order_id}
                    quant = replace_order(cancel_body,body)
                    if quant:
                        body['quantity'] = quant
                        print('calculated quantity is',body['quantity'])
                    else:
                        break
                    target_price=buy_sell_decision(body['side'].lower(),competitor_price,limit_threshold,current_order_id)
                    if target_price == "price range reached":
                        time.sleep(15)
                        continue
                    body['limitPrice'] = str(target_price)
                    latest_order_id = coinswitch.buy_limit_order(body).json() if side == 'buy' else coinswitch.sell_limit_order(body).json()
                    print('order info',latest_order_id)
                    print('new order placed.................')

                    
                    current_order_id = latest_order_id['data']['orderId'] 
                    current_placed_price = target_price
                    bot_message = "Re-adjusting position..."
                except Exception as e:
                    print(f"💥 CRASH AT BOTTOM OF REPLACE: {str(e)}") # Make sure you can see the error!
                    bot_message =f"error : {str(e)}"
                    bot_running = False
                    return
            else:
                print("✅ We are at the top of the book. Holding position.")

        except requests.exceptions.ConnectionError as e:
            print(f"📡 [NETWORK] Connection dropped in replace_order. Will retry. Error: {str(e)}")
            time.sleep(15)

        except Exception as e:
            print(f"An error occurred: {e}")
            bot_message = f"Error: {str(e)}"
            # Optional: Decide if you want bot_running = False here to kill it on network errors
        print('sleeping')
        time.sleep(3) # Wait before hitting the API again



#enddddddddddddddddddddddd

def dashboard(request):
    if not request.session.get('user'):
        return redirect('login')
        
    if request.method == "GET":
        return render(request, "dashboard.html")

    if request.method == "POST":
        api_action = request.POST.get('api')
        
        # Clean standard django/frontend keys from the payload
        body = {k: v for k, v in request.POST.items() if k not in ('api', 'csrfmiddlewaretoken')}
        
        try:
            # Dynamically call the matching function in coinswitch.py
            api_function = getattr(coinswitch, api_action)
            
            # Execute the function with the cleaned body payload
            response = api_function(body)
            
            try:
                data = response.json()
            except Exception:
                data = response.text
                
            return JsonResponse({"data": data, "status": response.status_code})
            
        except AttributeError:
            return JsonResponse({"error": f"API endpoint '{api_action}' not configured."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)