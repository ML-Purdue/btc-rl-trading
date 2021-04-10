import KrakenCredentials as cred
import KrakenAPI as krak

#https://github.com/dominiktraxl/pykrakenapi/blob/master/pykrakenapi/pykrakenapi.py

def test_private_methods():
  client = krak.KrakenClient(cred.api_key, cred.api_secret)
  print(client.get_ticker('BTC'))
  print(client.get_account_balance())
  print(client.get_trade_balance())
  return
  
def main():
  test_private_methods()
  return

if __name__ == '__main__':
  main()
  
