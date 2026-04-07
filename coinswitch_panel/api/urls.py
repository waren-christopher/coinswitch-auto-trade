from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', dashboard, name='dashboard'),
    #path('forgot-password/', forgot_password, name='forgot_password'),
    path("auto-trade/", auto_trade_page, name="auto_trade_page"),
    #   path('auto_trade', auto_trade, name='auto_trade'),
    path("auto-trade/", auto_trade_page),
    path("start-auto-trade", start_auto_trade),
    path("stop-auto-trade", stop_auto_trade),
    path("auto-trade-status", auto_trade_status),
]