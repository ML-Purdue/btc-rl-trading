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
    return {'refid': result['refid'], 
            'status': result['status'],
            'descr': result['descr']}

  def get_trade_history(self):
    result = self.conversion(self.client.query_private('TradesHistory', data= {'trades': 'true'}))
    return result

  def buy_market_order(self, ticker, volume):
    ticker = ticker + 'USD'
    ticker = ticker.upper()
    result = self.conversion(self.client.query_private('AddOrder', data={'pair': ticker, 'type':'buy', 'ordertype': 'market', 'volume': str(volume)}))['result']
    return {'descr': result['descr'], 'txid': result['txid']}
    
  def sell_market_order(self, ticker, volume):
    ticker = ticker + 'USD'
    ticker = ticker.upper()
    result = self.conversion(self.client.query_private('AddOrder', data={'pair': ticker, 'type':'sell', 'ordertype': 'market', 'volume': str(volume)}))['result']
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
  

