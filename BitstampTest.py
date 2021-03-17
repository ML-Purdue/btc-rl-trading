import BitstampMethods as btc
import credentials as cred



def main():

  tc_client = btc.BitstampTradingClient(cred.client_id, cred.api_key, cred.api_secret)
  print(tc_client.get_ticker())
  print(tc_client.get_order_book())
  print(tc_client.get_transaction())
  print(tc_client.get_balance())

if __name__ == '__main__':
  main()
