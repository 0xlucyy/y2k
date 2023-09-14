import os
from web3 import Web3
from dotenv import load_dotenv


try:
  dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
  load_dotenv(dotenv_path)
except:
   pass


class _Base(object):
  APP_NAME = 'y2k'
  # GOERLI_PROVIDER = os.environ.get("GOERLI_PROVIDER")
  MAINNET_PROVIDER = os.environ.get("MAINNET_PROVIDER")
  EMAIL = os.environ.get("EMAIL")
  PASSWORD = os.environ.get("PASSWORD")
  PRIV_KEY_ONE = os.environ.get("PRIV_KEY_ONE")

  BOND_FIXED_TERM_TELLER_ARBI_MAIN = Web3.toChecksumAddress('0x007F7A1cb838A872515c8ebd16bE4b14Ef43a222')

  DECIMAL_18 = 1000000000000000000

  CARRIERS = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
  }