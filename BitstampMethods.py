import requests
import time
import hashlib
import hmac
import json
import uuid
import sys

BASE_URL = 'http://www.bitstamp.net/api/v2'

TICKER_API_URL = '{}/ticker'.format(BASE_URL)
ORDER_BOOK_API_URL = '{}/order_book'.format(BASE_URL)
BALANCE_API_URL = '/api/v2/balance/'
TRANSACTIONS_API_URL = '/api/v2/user_transactions/'
CANCEL_ORDER_API_URL = '/api/v2/cancel_order/'
CANCEL_ALL_API_URL = '/api/v2/cancel_all_orders/'
ORDER_STATUS_API_URL = '/api/v2/order_status/'
OPEN_ORDERS_API_URL = '/api/v2/open_orders/all/'
BUY_MARKET_ORDER_API_URL = '/api/v2/buy/market/'
SELL_MARKET_ORDER_API_URL = '/api/v2/sell/market/'


def get_nonce():
    return str(uuid.uuid4())


def get_timestamp():
    return str(int(round(time.time() * 1000)))


class BitstampTradingClient():
    def __init__(self, username, public_key, secret_key):
        self.client_id = username
        self.api_key = public_key
        self.api_secret = bytes(secret_key, 'utf-8')

    def _get(self, url):
        req = requests.get(url).text
        resp = json.loads(req)
        return resp

    def generate_header(self, signature, content_type, nonce, timestamp):
        header = {
            'X-Auth': 'BITSTAMP ' + self.api_key,
            'X-Auth-Signature': signature,
            'X-Auth-Nonce': nonce,
            'X-Auth-Timestamp': timestamp,
            'X-Auth-Version': 'v2',
            'Content-Type': content_type
        }
        return header

    def generate_signature(self, message):
        signature = hmac.new(self.api_secret,
                             msg=message,
                             digestmod=hashlib.sha256)
        return signature.hexdigest()

    def api_output(self, payload, url):
        timestamp = get_timestamp()
        nonce = get_nonce()
        content_type = 'application/x-www-form-urlencoded'
        if sys.version_info.major >= 3:
            from urllib.parse import urlencode
        else:
            from urllib import urlencode
        payload_string = urlencode(payload)
        message = 'BITSTAMP ' + self.api_key + \
                'POST' + \
                'www.bitstamp.net' + \
                url + \
                '' + \
                content_type + \
                nonce + \
                timestamp + \
                'v2' + \
                payload_string
        message = message.encode('utf-8')
        signature = self.generate_signature(message=message)
        headers = self.generate_header(signature=signature,
                                       content_type=content_type,
                                       nonce=nonce,
                                       timestamp=timestamp)
        r = requests.post("https://www.bitstamp.net" + url,
                          headers=headers,
                          data=payload_string)
        if not r.status_code == 200:
            print(r.status_code)
            print(r.reason)
            raise Exception('Status code not 200')

        string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')
                          ).encode('utf-8') + r.content
        signature_check = self.generate_signature(message=string_to_sign)
        if not r.headers.get('X-Server-Auth-Signature') == signature_check:
            raise Exception('Signatures do not match')
        return json.loads((r.content).decode('utf-8'))

    def get_ticker(self, symbol='btc'):
        symbol = symbol + 'usd'
        url = '{}/{}/'.format(TICKER_API_URL, symbol)
        temp = self._get(url)
        ticker = {'last': temp['last'], 'bid': temp['bid'], 'ask': temp['ask']}
        return ticker

    def get_order_book(self, symbol='btc'):
        symbol = symbol + 'usd'
        url = '{}/{}/'.format(ORDER_BOOK_API_URL, symbol)
        temp = self._get(url)
        bids = temp['bids'][:5]
        asks = temp['asks'][:5]
        order_book = {'bids/buys': bids, 'asks/sells': asks}
        return order_book

    def get_balance(self):
        url = BALANCE_API_URL
        all_balances = self.api_output({'offset':'0'}, url)
        usd_balances = {}
        for key,value in all_balances.items():
          if 'balance' in key:
            usd_balances[key] = value
        return usd_balances


    def get_transaction(self, symbol='btc'):
        symbol = symbol + 'usd'
        url = '{}{}/'.format(TRANSACTIONS_API_URL, symbol)
        return self.api_output({
            'offset': '0',
            'limit': '100',
            'sort': 'desc'
        }, url)

    def cancel_order(self, order_id):
        url = CANCEL_ORDER_API_URL
        return self.api_output({'id': str(order_id)}, url)

    def cancel_all_orders(self):
        url = CANCEL_ALL_API_URL
        return self.api_output({'offset':'0'}, url)

    def get_open_status(self, order_id):
        url = ORDER_STATUS_API_URL
        return self.api_output({'id': str(order_id)}, url)

    def get_open_orders(self):
        url = OPEN_ORDERS_API_URL
        return self.api_output({'offset':'0'}, url)

    def market_buy_trade(self, amount, symbol=None):
        symbol = symbol + 'usd'
        url = '{}{}/'.format(BUY_MARKET_ORDER_API_URL, symbol)
        return self.api_output({'amount': str(amount)}, url)

    def market_sell_trade(self, amount, symbol=None):
        symbol = symbol + 'usd'
        url = '{}{}/'.format(SELL_MARKET_ORDER_API_URL, symbol)
        return self.api_output({'amount': str(amount)}, url)
