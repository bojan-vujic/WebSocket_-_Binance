from django.urls import path
from . import views

urlpatterns = [
    path('new_symbols/', views.new_symbols, name='new_symbols'),
    path('candlestick/', views.candlestick, name='candlestick'),
    path('price_monitoring/', views.price_monitoring, name='price_monitoring'),
    path('trades/', views.trades, name='trades'),
    path('trades_monitoring/', views.trades_monitoring, name='trades_monitoring'),
    
]


