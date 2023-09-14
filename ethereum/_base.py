from web3 import (
    Web3,
    HTTPProvider,
    WebsocketProvider,
    IPCProvider,
    middleware
)
from src.exceptions import (
    ProviderMissing,
    ProviderOffline
)
from src.config import _Base


class Web3_Base():
    def __init__(self, name: str = None):
        self.name = name if name else 'session0'
        self.w3 = Web3(self.get_provider())
        if self.w3.isConnected() == False:
            raise ProviderOffline('Provider is not online.')
    
    def add_middleware(self):
        pass

    def remove_middleware(self):
        pass

    def disconnect(self):
        if self.w3:
            self.w3 = None

    def get_provider(self):
        provider = _Base.MAINNET_PROVIDER
        # print(f'[INFO] Setting provider {provider} ...')
        # if app.config['ENV'] == 'live':
        #     provider = app.config["MAINNET_PROVIDER"]
        # else:
        #     provider = app.config["INFURA_PROVIDER"]
        if provider:
            if 'http' in provider:
                return HTTPProvider(provider)
            elif 'ws' in provider:
                return WebsocketProvider(provider)
            elif '.ipc' in provider:
                return IPCProvider(provider)
        raise ProviderMissing('Invalid Provider. Set in settings.py.')


# test = Web3_Base()
# import pdb; pdb.set_trace()
# print('holding...')