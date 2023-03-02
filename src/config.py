import os
from web3 import Web3
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


'''
'''
class _Base(object):
    APP_NAME = 'y2k'
    GOERLI_PROVIDER = os.environ.get("GOERLI_PROVIDER")
    MAINNET_PROVIDER = os.environ.get("MAINNET_PROVIDER")
    # API_URI = os.environ.get("API_URI")
    # RETRY_LIMIT = os.environ.get("RETRY_LIMIT")
    FLOWERS_PRIV_KEY = os.environ.get("FLOWERS_PRIV_KEY")

    FIXED_TERM_AUCTIONEER_ARBI_MAIN = Web3.toChecksumAddress('0x007F7A1cb838A872515c8ebd16bE4b14Ef43a222')

    DECIMAL_18 = 1000000000000000000