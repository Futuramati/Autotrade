from __future__ import print_function
from flask import Flask, render_template, request, flash, redirect, jsonify
from flask import request
from flask_sse import sse
# from DateTime import Timezones
from datetime import datetime
# from flask_cors import CORS, cross_origin
from binance.client import Client
from binance.enums import *
from websocket import WebSocketApp
import time
import config, csv, datetime
import websocket, json
import sys
import datetime
from datetime import datetime as dt
from jinja2 import Markup


app = Flask(__name__)

# cors = CORS(app)
app.secret_key = b'defwqgrjhgklfkvhgxdtfuyghnjk'

client = Client(config.API_KEY, config.API_SECRET)

#socket = f'wss://stream.binance.com:9443/ws/dashusdt@depth5'

choosed_symbol = 'DASH'
changed_base = 'BUSD'
choosed_pair = choosed_symbol+'BTC'
timestamp = 1545730073
x = dt.now()
dt_object = dt.fromtimestamp(timestamp)


def clever_function(timestamp):
    # timestamp = 0
    dt_object = dt.fromtimestamp(timestamp)
    return dt_object
app.jinja_env.globals.update(clever_function=clever_function)


@app.route('/', methods=['POST'])
def send_choose():
    print(request.form)
    global choosed_pair
    global choosed_symbol
    choosed_pair = request.form['pair_choosed']
    choosed_symbol = request.form['my_cryptocoin']
    return redirect('/')

@app.route('/')
# @cross_origin()
def index():

  #  choosed_pair = request.form['symbol_choosed']

    title = choosed_pair

    coin = choosed_symbol

    account_info = client.get_account()
    balances = account_info['balances']
    # free_balance = account_info['free']

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    fees = client.get_trade_fee(symbol=choosed_pair)
    #fees = client.get_trade_fee()
    #tradeFee = fees['tradeFee']

 #   price_BNBUSDT = client.get_recent_trades(symbol='BNBUSDT',limit='1')

    orders = client.get_open_orders()

  #  depth = client.get_order_book(symbol='BNBBTC')
    #tradesBUSD = client.get_my_trades(symbol='BNBBUSD')

    try:
       tradesUSDT= client.get_my_trades(symbol=choosed_symbol+"USDT", limit=5)
       depthUSDT = client.get_order_book(symbol=choosed_symbol+"USDT", limit=5)
    except:
        tradesUSDT= ""
        depthUSDT= ""
    try:
       tradesBTC= client.get_my_trades(symbol=choosed_symbol+"BTC", limit=5)
       depthBTC = client.get_order_book(symbol=choosed_symbol+"BTC", limit=5)
    except:
        tradesBTC= ""
        depthBTC= ""
    try:
       tradesBNB= client.get_my_trades(symbol=choosed_symbol+"BNB", limit=5)
       depthBNB = client.get_order_book(symbol=choosed_symbol+"BNB", limit=5)
    except:
        tradesBNB= ""
        depthBNB= ""
    try:
        tradesETH= client.get_my_trades(symbol=choosed_symbol+"ETH", limit=5)
        depthETH = client.get_order_book(symbol=choosed_symbol+"ETH", limit=5)
    except:
        tradesETH= ""
        depthETH= ""
     
    time.sleep(1)

    return render_template('index.html', dt_object=dt_object, title=title, coin=coin, my_orders=orders, my_balances=balances, symbols=symbols, my_fees=fees, depth_USDT=depthUSDT, depth_BTC=depthBTC, my_trades_USDT=tradesUSDT, my_trades_BTC=tradesBTC, my_trades_ETH=tradesETH, my_trades_BNB=tradesBNB)



# if __name__ == "__main__":
#     app.run(host='localhost', port=5000)
@app.route('/cancel', methods=['POST'])
def cancel():
    print(request.form)
    try:
        cancel = client.cancel_order(
            symbol=request.form['orderSymbol'],
            orderId=request.form['orderID'])

    except Exception as e:
        flash(e.message, "error")

    return redirect('/')



@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
         order = client.create_order(
            symbol=request.form['symbolbuy'],
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=request.form['quantitybuy'],
            price=request.form['buyprice'])

    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/sell', methods=['POST'])
def sell():
    print(request.form)
    try:
         order = client.create_order(
            symbol=request.form['symbolsell'],
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=request.form['quantitysell'],
            price=request.form['sellprice'])

    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/settings')
def settings():
    return 'settings'


@app.route('/history')
def history():
    candlesticks = client.get_klines(symbol=choosed_pair, interval=Client.KLINE_INTERVAL_15MINUTE)
   # client.get_historical_klines("ETCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Dec, 2020", "26 Fev, 2021")
    #candles = client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
            }
        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)

@app.route('/history_USDT')
def history_USDT():
    candlesticks = client.get_klines(symbol=choosed_symbol+'USDT', interval=Client.KLINE_INTERVAL_15MINUTE)
   # client.get_historical_klines("ETCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Dec, 2020", "26 Fev, 2021")
    #candles = client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
            }
        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)
