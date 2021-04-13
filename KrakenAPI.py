import krakenex as nex
import json
#disable two factor password

#the account needs funding

class KrakenClient():
  def __init__(self, api_key, api_secret):
    self.api_key = api_key
    self.api_secret = api_secret
    self.client = nex.API(key=self.api_key, secret=self.api_secret)
  
  def conversion(self, text):
    result = json.dumps(text)
    out = json.loads(result)
    return out

  def get_minimum_order_size(self, ticker):
    ticker = ticker.upper()
    order_size = {'AAVE': '0.05',
                  'ALGO': '15',
                  'ANT': '2',
                  'REP': '0.3',
                  'REPV2': '0.3',
                  'BAL': '0.3',
                  'BAT': '30',
                  'BTC': '0.0002',
                  'BCH': '0.02',
                  'ADA': '25',
                  'LINK': '0.5',
                  'COMP': '0.05',
                  'ATOM': '1',
                  'CRV': '10',
                  'DAI': '5',
                  'DASH': '0.05',
                  'MANA': '50',
                  'DOGE': '50',
                  'EWT': '1',
                  'EOS': '2.5',
                  'ETH': '0.005',
                  'ETH2.S': '0.02',
                  'ETC': '1',
                  'FIL': '0.3',
                  'FLOW': '1',
                  'GNO': '0.05',
                  'ICX': '10',
                  'KAVA': '5',
                  'KEEP': '25',
                  'KSM': '0.1',
                  'KNC': '5',
                  'LSK': '5',
                  'LTC': '0.05',
                  'MLN': '0.2',
                  'XMR': '0.05',
                  'NANO': '2',
                  'OCEAN': '10',
                  'OMG': '2',
                  'OXT': '25',
                  'PAXG': '0.004',
                  'DOT': '0.5',
                  'QTUM': '2.5',
                  'XRP': '20',
                  'SC': '1500',
                  'XLM': '20',
                  'STORJ': '20',
                  'SNX': '0.5',
                  'TBTC': '0.0002',
                  'USDT': '5',
                  'XTZ': '3',
                  'GRT': '20',
                  'TRX': '250',
                  'UNI': '1',
                  'USDC': '5',
                  'WAVES': '2',
                  'YFI': '0.0002',
                  'ZEC': '0.1',
                  'EUR': '5',
                  'USD': '10',
                  'GBP': '5',
                  'AUD': '10'}
    return float(order_size[ticker])
  
  def get_account_balance(self):
    balance = self.conversion(self.client.query_private('Balance'))
    try:
      balance = balance['result']
    except:
      return {'error': balance['error'], 'balance': 0}
    return balance

  def get_ticker(self, ticker):
    ticker = ticker + "USD"
    ticker = ticker.upper()
    result = self.conversion(nex.API().query_public('Ticker', data={'pair' : ticker}))["result"]
    var = list(result.keys())[0]
    result = result[str(var)]
    return {'name': ticker, 
            'ask': float(result["a"][0]), 
            'bid': float(result["b"][0]), 
            'last': float(result["c"][0])}
  
  def get_trade_balance(self):
    result = self.conversion(self.client.query_private('TradeBalance'))
    try:
      result = result['result']
    except:
      return {'error': result['error'], 'equivalent': 0, 'trade': 0, 'p/l': 0}
    return {'equivalent': result['eb'], 
            'trade':result['tb'],
            'p/l': result['n']}

  def get_open_orders(self):
    result = self.conversion(self.client.query_private('OpenOrders', data= {'trades': 'true'}))["result"]
    return result['open']

  def get_closed_orders(self):
    result = self.conversion(self.client.query_private('ClosedOrders', data= {'trades':'true'}))['result']
    return result['closed']

  def get_trade_history(self):
    result = self.conversion(self.client.query_private('TradesHistory', data= {'trades': 'true'}))['result']
    return result['trades']

  def buy_market_order(self, ticker, volume):
    if volume < self.get_minimum_order_size(ticker):
      return {'error': 'not a valid order size'}
    ticker = ticker + 'USD'
    ticker = ticker.upper()
    result = self.conversion(self.client.query_private('AddOrder', data={'pair': ticker, 'type':'buy', 'ordertype': 'market', 'volume': str(volume), 'leverage': 'none', 'starttm': '0', 'expiretm':'+86400'}))['result']
    return {'descr': result['descr'], 'txid': result['txid']}
    #return {'descr': result['descr'], 'txid': result['txid']}
    
  def sell_market_order(self, ticker, volume):
    if volume < self.get_minimum_order_size(ticker):
      return {'error': 'not a valid order size'}
    ticker = ticker + 'USD'
    ticker = ticker.upper()
    result = self.conversion(self.client.query_private('AddOrder', data={'pair': ticker, 'type':'sell', 'ordertype': 'market', 'volume': str(volume), 'leverage': 'none', 'starttm': '0', 'expiretm':'+86400'}))['result']
    return {'descr': result['descr'], 'txid': result['txid']}

  def trade_status(self, txid):
    result = self.conversion(self.client.query_private('QueryOrders', data= {'txid': txid, 'trades': 'true'}))
    try:
      result = result['result']
    except:
      return {'error': result['error']}
    return result
    #return {'status': result['status'], 'descr': result['decsr'], 'refid': result['refid'], 'userref': result['userref']}
    
  def cancel_open_order(self, txid):
    result = self.conversion(self.client.query_private('CancelOrder', data= {'txid' : str(txid)}))['result']
    return {'count': result['count'], 'pending': result['pending']}
  

