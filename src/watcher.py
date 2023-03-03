import json
import requests
from datetime import datetime
from src.config import _Base
from ethereum._base import Web3_Base
from graphql.queries import MARKETS
from pprint import pprint
from src.sender import send_message
# import pdb;pdb.set_trace()

def main():
  print(f'\n[{datetime.now()}]  Gathering bond market data ...')
  configs = _Base()
  bond_metadata = {}
  w3_obj = Web3_Base()

  # abiFile = json.load(open('./ethereum/abis/FIXED_TERM_AUCTIONEER_ARBI_MAIN.json'))
  abiFile = {
	"abi": [{
		"inputs": [{
			"internalType": "contract IBondTeller",
			"name": "teller_",
			"type": "address"
		}, {
			"internalType": "contract IBondAggregator",
			"name": "aggregator_",
			"type": "address"
		}, {
			"internalType": "address",
			"name": "guardian_",
			"type": "address"
		}, {
			"internalType": "contract Authority",
			"name": "authority_",
			"type": "address"
		}],
		"stateMutability": "nonpayable",
		"type": "constructor"
	}, {
		"inputs": [],
		"name": "Auctioneer_AmountLessThanMinimum",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_BadExpiry",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_InitialPriceLessThanMin",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_InvalidCallback",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_InvalidParams",
		"type": "error"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "conclusion_",
			"type": "uint256"
		}],
		"name": "Auctioneer_MarketConcluded",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_MaxPayoutExceeded",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_NewMarketsNotAllowed",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_NotAuthorized",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_NotEnoughCapacity",
		"type": "error"
	}, {
		"inputs": [],
		"name": "Auctioneer_OnlyMarketOwner",
		"type": "error"
	}, {
		"anonymous": False,
		"inputs": [{
			"indexed": True,
			"internalType": "address",
			"name": "user",
			"type": "address"
		}, {
			"indexed": True,
			"internalType": "contract Authority",
			"name": "newAuthority",
			"type": "address"
		}],
		"name": "AuthorityUpdated",
		"type": "event"
	}, {
		"anonymous": False,
		"inputs": [{
			"indexed": False,
			"internalType": "uint32",
			"name": "defaultTuneInterval",
			"type": "uint32"
		}, {
			"indexed": False,
			"internalType": "uint32",
			"name": "defaultTuneAdjustment",
			"type": "uint32"
		}, {
			"indexed": False,
			"internalType": "uint32",
			"name": "minDebtDecayInterval",
			"type": "uint32"
		}, {
			"indexed": False,
			"internalType": "uint32",
			"name": "minDepositInterval",
			"type": "uint32"
		}, {
			"indexed": False,
			"internalType": "uint32",
			"name": "minMarketDuration",
			"type": "uint32"
		}, {
			"indexed": False,
			"internalType": "uint32",
			"name": "minDebtBuffer",
			"type": "uint32"
		}],
		"name": "DefaultsUpdated",
		"type": "event"
	}, {
		"anonymous": False,
		"inputs": [{
			"indexed": True,
			"internalType": "uint256",
			"name": "id",
			"type": "uint256"
		}],
		"name": "MarketClosed",
		"type": "event"
	}, {
		"anonymous": False,
		"inputs": [{
			"indexed": True,
			"internalType": "uint256",
			"name": "id",
			"type": "uint256"
		}, {
			"indexed": True,
			"internalType": "address",
			"name": "payoutToken",
			"type": "address"
		}, {
			"indexed": True,
			"internalType": "address",
			"name": "quoteToken",
			"type": "address"
		}, {
			"indexed": False,
			"internalType": "uint48",
			"name": "vesting",
			"type": "uint48"
		}, {
			"indexed": False,
			"internalType": "uint256",
			"name": "initialPrice",
			"type": "uint256"
		}],
		"name": "MarketCreated",
		"type": "event"
	}, {
		"anonymous": False,
		"inputs": [{
			"indexed": True,
			"internalType": "address",
			"name": "user",
			"type": "address"
		}, {
			"indexed": True,
			"internalType": "address",
			"name": "newOwner",
			"type": "address"
		}],
		"name": "OwnerUpdated",
		"type": "event"
	}, {
		"anonymous": False,
		"inputs": [{
			"indexed": True,
			"internalType": "uint256",
			"name": "id",
			"type": "uint256"
		}, {
			"indexed": False,
			"internalType": "uint256",
			"name": "oldControlVariable",
			"type": "uint256"
		}, {
			"indexed": False,
			"internalType": "uint256",
			"name": "newControlVariable",
			"type": "uint256"
		}],
		"name": "Tuned",
		"type": "event"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"name": "adjustments",
		"outputs": [{
			"internalType": "uint256",
			"name": "change",
			"type": "uint256"
		}, {
			"internalType": "uint48",
			"name": "lastAdjustment",
			"type": "uint48"
		}, {
			"internalType": "uint48",
			"name": "timeToAdjusted",
			"type": "uint48"
		}, {
			"internalType": "bool",
			"name": "active",
			"type": "bool"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "allowNewMarkets",
		"outputs": [{
			"internalType": "bool",
			"name": "",
			"type": "bool"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "authority",
		"outputs": [{
			"internalType": "contract Authority",
			"name": "",
			"type": "address"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "address",
			"name": "",
			"type": "address"
		}],
		"name": "callbackAuthorized",
		"outputs": [{
			"internalType": "bool",
			"name": "",
			"type": "bool"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "closeMarket",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "bytes",
			"name": "params_",
			"type": "bytes"
		}],
		"name": "createMarket",
		"outputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "currentCapacity",
		"outputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "currentControlVariable",
		"outputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "currentDebt",
		"outputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "defaultTuneAdjustment",
		"outputs": [{
			"internalType": "uint32",
			"name": "",
			"type": "uint32"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "defaultTuneInterval",
		"outputs": [{
			"internalType": "uint32",
			"name": "",
			"type": "uint32"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "getAggregator",
		"outputs": [{
			"internalType": "contract IBondAggregator",
			"name": "",
			"type": "address"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "getMarketInfoForPurchase",
		"outputs": [{
			"internalType": "address",
			"name": "owner",
			"type": "address"
		}, {
			"internalType": "address",
			"name": "callbackAddr",
			"type": "address"
		}, {
			"internalType": "contract ERC20",
			"name": "payoutToken",
			"type": "address"
		}, {
			"internalType": "contract ERC20",
			"name": "quoteToken",
			"type": "address"
		}, {
			"internalType": "uint48",
			"name": "vesting",
			"type": "uint48"
		}, {
			"internalType": "uint256",
			"name": "maxPayout",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "getTeller",
		"outputs": [{
			"internalType": "contract IBondTeller",
			"name": "",
			"type": "address"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "isInstantSwap",
		"outputs": [{
			"internalType": "bool",
			"name": "",
			"type": "bool"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "isLive",
		"outputs": [{
			"internalType": "bool",
			"name": "",
			"type": "bool"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "marketPrice",
		"outputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "marketScale",
		"outputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"name": "markets",
		"outputs": [{
			"internalType": "address",
			"name": "owner",
			"type": "address"
		}, {
			"internalType": "contract ERC20",
			"name": "payoutToken",
			"type": "address"
		}, {
			"internalType": "contract ERC20",
			"name": "quoteToken",
			"type": "address"
		}, {
			"internalType": "address",
			"name": "callbackAddr",
			"type": "address"
		}, {
			"internalType": "bool",
			"name": "capacityInQuote",
			"type": "bool"
		}, {
			"internalType": "uint256",
			"name": "capacity",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "totalDebt",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "minPrice",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "maxPayout",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "sold",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "purchased",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "scale",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}, {
			"internalType": "address",
			"name": "referrer_",
			"type": "address"
		}],
		"name": "maxAmountAccepted",
		"outputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"name": "metadata",
		"outputs": [{
			"internalType": "uint48",
			"name": "lastTune",
			"type": "uint48"
		}, {
			"internalType": "uint48",
			"name": "lastDecay",
			"type": "uint48"
		}, {
			"internalType": "uint32",
			"name": "length",
			"type": "uint32"
		}, {
			"internalType": "uint32",
			"name": "depositInterval",
			"type": "uint32"
		}, {
			"internalType": "uint32",
			"name": "tuneInterval",
			"type": "uint32"
		}, {
			"internalType": "uint32",
			"name": "tuneAdjustmentDelay",
			"type": "uint32"
		}, {
			"internalType": "uint32",
			"name": "debtDecayInterval",
			"type": "uint32"
		}, {
			"internalType": "uint256",
			"name": "tuneIntervalCapacity",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "tuneBelowCapacity",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "lastTuneDebt",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "minDebtBuffer",
		"outputs": [{
			"internalType": "uint32",
			"name": "",
			"type": "uint32"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "minDebtDecayInterval",
		"outputs": [{
			"internalType": "uint32",
			"name": "",
			"type": "uint32"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "minDepositInterval",
		"outputs": [{
			"internalType": "uint32",
			"name": "",
			"type": "uint32"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "minMarketDuration",
		"outputs": [{
			"internalType": "uint32",
			"name": "",
			"type": "uint32"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"name": "newOwners",
		"outputs": [{
			"internalType": "address",
			"name": "",
			"type": "address"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [],
		"name": "owner",
		"outputs": [{
			"internalType": "address",
			"name": "",
			"type": "address"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "ownerOf",
		"outputs": [{
			"internalType": "address",
			"name": "",
			"type": "address"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "amount_",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}, {
			"internalType": "address",
			"name": "referrer_",
			"type": "address"
		}],
		"name": "payoutFor",
		"outputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"stateMutability": "view",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}],
		"name": "pullOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "amount_",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "minAmountOut_",
			"type": "uint256"
		}],
		"name": "purchaseBond",
		"outputs": [{
			"internalType": "uint256",
			"name": "payout",
			"type": "uint256"
		}],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}, {
			"internalType": "address",
			"name": "newOwner_",
			"type": "address"
		}],
		"name": "pushOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "bool",
			"name": "status_",
			"type": "bool"
		}],
		"name": "setAllowNewMarkets",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "contract Authority",
			"name": "newAuthority",
			"type": "address"
		}],
		"name": "setAuthority",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "address",
			"name": "creator_",
			"type": "address"
		}, {
			"internalType": "bool",
			"name": "status_",
			"type": "bool"
		}],
		"name": "setCallbackAuthStatus",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint32[6]",
			"name": "defaults_",
			"type": "uint32[6]"
		}],
		"name": "setDefaults",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "id_",
			"type": "uint256"
		}, {
			"internalType": "uint32[3]",
			"name": "intervals_",
			"type": "uint32[3]"
		}],
		"name": "setIntervals",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "address",
			"name": "newOwner",
			"type": "address"
		}],
		"name": "setOwner",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}, {
		"inputs": [{
			"internalType": "uint256",
			"name": "",
			"type": "uint256"
		}],
		"name": "terms",
		"outputs": [{
			"internalType": "uint256",
			"name": "controlVariable",
			"type": "uint256"
		}, {
			"internalType": "uint256",
			"name": "maxDebt",
			"type": "uint256"
		}, {
			"internalType": "uint48",
			"name": "vesting",
			"type": "uint48"
		}, {
			"internalType": "uint48",
			"name": "conclusion",
			"type": "uint48"
		}],
		"stateMutability": "view",
		"type": "function"
	}]
}
  abi = abiFile['abi']
  teller_contract = w3_obj.w3.eth.contract(
      abi=abi,
      address=configs.FIXED_TERM_AUCTIONEER_ARBI_MAIN,
  )

  # get all y2k markets from graphql.
  markets = requests.post(
    url='https://api.thegraph.com/subgraphs/name/bond-protocol/bond-protocol-arbitrum-mainnet',
    json={"query": MARKETS}
  )
  # Extract all market data.
  markets = (markets.json())['data']['markets']

  # get y2k market price from coingecko.
  data = {'ids': 'y2k', 'vs_currencies': 'usd'}
  y2k_price = requests.get(
    url='https://api.coingecko.com/api/v3/simple/price',
    params=data
  )
  # Extract usd price.
  y2k_price = (y2k_price.json())['y2k']['usd']

  for market in markets:
    market_id = market['marketId']
    live = teller_contract.functions.isLive(int(market_id)).call()

    if live == True:
      market_info = teller_contract.functions.getMarketInfoForPurchase(id_=int(market_id)).call()
      bond_price = teller_contract.functions.marketPrice(id_=int(market_id)).call()

      # Max purchase amount of Y2K
      max_payout = (market_info[-1] / configs.DECIMAL_18)

      # Price of bond in USD
      bond_price = (bond_price / configs.DECIMAL_18)
      bond_price = str(bond_price)[0:5]

      # Calc bond discount.
      discount = (((float(bond_price) / float(y2k_price)) * 100) - 100) * -1

      bond_metadata[market_id] = {
        'bond_price': bond_price,
        'y2k_price': y2k_price,
        'max_payout': max_payout,
        'discount': discount,
        'url': f'https://app.bondprotocol.finance/#/market/42161/{market_id}'
      }

      if float(bond_metadata[market_id]['discount']) > 9.99:
        print(f"[INFO]  Sending text alert ...")
        send_message('7142228402', 'tmobile', "Discount is over 9.99%")

  pprint(bond_metadata)

main()