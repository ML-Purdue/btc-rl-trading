import credentials as cred
import KrakenAPI as krak

def test_private_methods():
  client = krak.KrakenClient(cred.api_key, cred.api_secret)
  print(client.get_trade_history())
  print('\n')
  print(client.get_closed_orders())
  print('\n')
  print(client.get_ticker('BTC'))
  print('\n')
  print(client.get_account_balance())
  print('\n')
  print(client.get_trade_balance())
  print('\n')
  #print(client.buy_market_order('USDC', 5))
  print('\n')
  #print(client.sell_market_order('USDC', 5))
  return
  
def main():
  test_private_methods()
  return

if __name__ == '__main__':
  main()
