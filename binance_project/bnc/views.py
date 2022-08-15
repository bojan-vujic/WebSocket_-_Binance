from hashlib import new
from django.shortcuts import render
from .models import Symbol
from binance import Client
import json



def new_symbols(request):

  client  = Client()
  tickers = client.get_all_tickers()
  symbols = [i['symbol'] for i in tickers]
  prices  = [float(i['price']) for i in tickers]
  new_data = {
    'symbols' : symbols,
    'prices' : prices
  }

  num_symbols = len(symbols)
  item, created = Symbol.objects.get_or_create(user=request.user)

  if created:
    item.user   = request.user
    item.symbols = json.dumps(new_data, indent = 2)
    item.save()
    context = {
      'title' : 'Total number of symbols : %i' % num_symbols,
    }
  else:
    existing = Symbol.objects.filter(user=request.user).values()
    json_data = existing[0]['symbols'].replace("'", "\"")
    old_symbols = json.loads(json_data)['symbols']
    item.symbols = json.dumps(new_data, indent = 2)
    item.save()

    new_data = list(set(symbols) - set(old_symbols))
    new_symbols = [
      {'symbol':value, 'price':prices[i]}
      for i, value in enumerate(symbols) if value in new_data
    ]
    length_symbols = len(new_symbols)
    if length_symbols == 0:
      title = 'No new symbols since your last visit'
    elif length_symbols == 1:
      title = 'There is %i new symbol since your last visit' % length_symbols
    else:
      title = 'There are %i new symbols since your last visit' % length_symbols

    context = {
      'title' : title,
      'new_symbols' : new_symbols,
      'new_symbols_str' : ', '.join([str(i) for i in new_symbols])
    }

  return render(request, 'bnc/symbols.html', context)


def candlestick(request):
  return render(request, 'bnc/candlestick.html', {})

def trades(request):
  return render(request, 'bnc/trades.html', {})


def price_monitoring(request):
  context = {}
  if request.method == "POST":
    symbol    = request.POST.get('symbol').lower()
    min_price = request.POST.get('price')
    interval  = request.POST.get('interval')
    limit     = request.POST.get('limit')

    data, data_min = [], []
    raw_data = Client().get_klines(symbol=symbol.upper(), interval=interval, limit = limit)
    for i in raw_data:
      data_min.append({ 'time' :  i[0]/1000, 'value' : min_price })
      obj = { 'time' : i[0]/1000, 'open' : i[1], 'high' : i[2], 'low' : i[3], 'close' : i[4]}
      data.append(obj)
      

    print('length : ', len(data))
    context = {
      'symbol' : symbol,
      'min_price' : min_price,
      'interval' : interval,
      'limit' : limit,
      'data' : json.dumps(data),
      'data_min' : json.dumps(data_min),
    }
  
  return render(request, 'bnc/candlestick_charts.html', context)
  

def trades_monitoring(request):
  context = {}
  if request.method == "POST":
    symbol    = request.POST.get('symbol').lower()
    min_price = request.POST.get('price')
    context = {
      'symbol' : symbol,
      'min_price' : min_price,
    }

  return render(request, 'bnc/trades-partial.html', context)