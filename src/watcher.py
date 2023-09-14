import requests
import json
from src.config import _Base
from src.sender import send_message
from ethereum._base import Web3_Base
from graphql.queries import MARKETS
from pprint import pprint
from datetime import datetime
# import pdb;pdb.set_trace()


'''
An actual cron job. This job can be activated
or deactivated with cronLob.py. There is a working
example of activating this cron.
'''



MARKETS_TO_SEARCH = ['Pendle', 'Y2K']

def bond_protocol_watcher():
  print(f'\n[{datetime.now()}]  Gathering bond market data ...')
  configs = _Base()
  bond_metadata = {}
  w3_obj = Web3_Base()
  markets = []

  abiFile = json.load(open('./ethereum/abis/FIXED_TERM_AUCTIONEER_ARBI_MAIN.json'))

  abi = abiFile['abi']
  teller_contract = w3_obj.w3.eth.contract(
      abi=abi,
      address=configs.FIXED_TERM_AUCTIONEER_ARBI_MAIN,
  )
  
  for _market in MARKETS_TO_SEARCH:
    replacement = f'name:"{_market}"'
    payload = requests.post(
			url='https://api.thegraph.com/subgraphs/name/bond-protocol/bond-protocol-arbitrum-mainnet',
			json={"query": MARKETS.replace('name:"_NAME"', replacement)}
		)
    markets.extend((payload.json())['data']['markets'])

  # get y2k & pendle market price from coingecko.
  data = {'ids': 'y2k,pendle', 'vs_currencies': 'usd'}
  prices = requests.get(
    url='https://api.coingecko.com/api/v3/simple/price',
    params=data
  )

  # Extract usd price.
  try:
    y2k_price = (prices.json())['y2k']['usd']
    pendle_price = (prices.json())['pendle']['usd']
    print("[INFO]  " + "Y2K Price".ljust(8, " ") + ": " + str(y2k_price))
    print("[INFO]  " + "Pendle Price".ljust(8, " ") + ": " + str(pendle_price))
  except KeyError as KE:
    print(f"[ERROR] y2k_price: {y2k_price} ...")
    return 666
  if markets == []:
    print(f"No active bonds")
    return 0
      
  for market in markets:
    market_id = market['marketId']
    live = teller_contract.functions.isLive(int(market_id)).call()

    if live == True:
      market_info = teller_contract.functions.getMarketInfoForPurchase(id_=int(market_id)).call()
      bond_price = teller_contract.functions.marketPrice(id_=int(market_id)).call()

      # Max purchase amount.
      max_payout = (market_info[-1] / configs.DECIMAL_18)

      # Price of bond in USD
      bond_price = (bond_price / configs.DECIMAL_18)
      bond_price = str(bond_price)[0:5]

      # import pdb;pdb.set_trace()
      if market['payoutToken']['name'].lower() == 'pendle':
        continue
        discount = (((float(bond_price) / float(pendle_price)) * 100) - 100) * -1
      else:
        discount = (((float(bond_price) / float(y2k_price)) * 100) - 100) * -1

      bond_metadata[market_id] = {
        'market': market['name'],
				'bond_price': bond_price,
        'y2k_price': y2k_price,
        'max_payout': max_payout,
        'discount': discount,
        'url': f'https://app.bondprotocol.finance/#/market/42161/{market_id}'
      }

      if float(bond_metadata[market_id]['discount']) >= 6:
        print(f"[INFO]  Sending text alert ...")
        send_message('7142228402', 'tmobile', f"Discount is {bond_metadata[market_id]['discount']}%")

      marid = 'MarketId'
      dis = 'Discount'
      maxpay = 'MaxPay'
      bprice = 'Bond Price'
      _name = market['payoutToken']['name']
      __name = 'Market'
      print(f'{__name.ljust(10, " ")}: {_name}')
      print(f'{marid.ljust(10, " ")}: {market_id}')
      print(f'{dis.ljust(10, " ")}: {discount}')
      print(f'{maxpay.ljust(10, " ")}: {max_payout}')
      print(f'{bprice.ljust(10, " ")}: {bond_price}')
      print("*"*35)
  pprint(bond_metadata)
