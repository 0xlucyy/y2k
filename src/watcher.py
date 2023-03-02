import json
import requests
from src.config import _Base
from ethereum._base import Web3_Base
from graphql.queries import MARKETS
# import pdb;pdb.set_trace()

def main():
  configs = _Base()

  print('HELLO FROM AUTOMATION')

  w3_obj = Web3_Base()

  abiFile = json.load(open('./ethereum/abis/FIXED_TERM_AUCTIONEER_ARBI_MAIN.json'))
  abi = abiFile['abi']
  teller_contract = w3_obj.w3.eth.contract(
      abi=abi,
      address=configs.FIXED_TERM_AUCTIONEER_ARBI_MAIN,
  )

  # get all y2k markets from graphql.
  response = requests.post(
    url='https://api.thegraph.com/subgraphs/name/bond-protocol/bond-protocol-arbitrum-mainnet',
    json={"query": MARKETS}
  )
  # Extract all market data.
  payload = (response.json())['data']['markets']

  # # get y2k market price from coingecko.
  # data = {'ids': 'y2k', 'vs_currencies': 'usd'}
  # y2k_price = requests.get(
  #   url='https://api.coingecko.com/api/v3/simple/price',
  #   params=data
  # )
  # # Extract usd price.
  # y2k_price = (y2k_price.json())['y2k']['usd']

  # import pdb;pdb.set_trace()

  for market in payload:
    market_id = market['marketId']

    print(f"Checking market # {market_id}")
    live = teller_contract.functions.isLive(int(market_id)).call()

    if live == True:
      print('Market is live!!!!!')
      # market_info = teller_contract.functions.getMarketInfoForPurchase(id_=int(market_id)).call()
      # bond_price = teller_contract.functions.marketPrice(id_=int(market_id)).call()

      # # Max purchase amount of Y2K
      # max_payout = (market_info[-1] / configs.DECIMAL_18)

      # # Price of bond in USD
      # bond_price = (bond_price / configs.DECIMAL_18)
      # bond_price = str(bond_price)[0:5]

      # print(f"Bond Price: {bond_price}")
      # # print(f"Y2K Price: {y2k_price}")
      # print(f"Max Payout: {max_payout}")
    else:
      print('Market is not live')
    
  import pdb;pdb.set_trace()


  print('hold')

