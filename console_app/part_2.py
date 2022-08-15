#
# Websocket for binance api
#
import pandas as pd  # just to convert time (you can comment this line)
import os            # optional, just to clear the terminal
import websocket
import json

symbol       = 'BTCUSDT'   # symbol to track
interval     = '1m'        # interval  : 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
price_tag    = 'o'         # o, c, l, h (chose which to track)
min_price    = 23000
convert_time = True


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    if os.name == 'posix':
        os.system('clear')

def on_open(ws):
    subscribe = {
        "method": "SUBSCRIBE",
        "params": ["%s@kline_%s" % (symbol.lower(), interval.lower())], "id": 1
    }
    ws.send(json.dumps(subscribe))

def on_message(ws, message):
    data = json.loads(message)
    clear_console()
    try:
        if float(data['k'][price_tag]) > min_price:
            if convert_time:
                t = str(pd.to_datetime(int(data['k']['t']), unit='ms'))
            else:
                t = int(data['k']['t'])
            o = float(data['k']['o']) # open price
            c = float(data['k']['c']) # closed
            h = float(data['k']['h']) # high
            l = float(data['k']['l']) # low
            avg = (o + c)/2           # average
            
            new_data = {
                't' : t,
                'o' : o,
                'c' : c,
                'h' : h,
                'l' : l,
                'avg' : avg
            }
            print('Current price %f > %f' % (new_data[price_tag], min_price))
            print(json.dumps(new_data, indent = 2))
        else:
            print('NOPE')
    except Exception as ex:
        print(ex)

url = 'wss://stream.binance.com:9443/ws'
ws  = websocket.WebSocketApp(url, on_open = on_open, on_message = on_message)
ws.run_forever()
