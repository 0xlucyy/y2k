
from typing import Tuple
from web3 import (
    Web3
)
from web3.exceptions import (
    TimeExhausted,
    # ContractLogicError
)
# from backend.models.models import Domains
# import pdb; pdb.set_trace()


'''
Returns:
    (Bool, Str) : True/False, Either err msg or transaction hash
'''
def SIGN_SEND_WAIT(w3: Web3 = None, transaction: dict = None, FLOWERS_PRIV_KEY: str = None) -> Tuple[bool, str]:
    signed_tx = w3.eth.account.sign_transaction(transaction, FLOWERS_PRIV_KEY)

    try:
        tx_hash = w3.eth.send_raw_transaction(transaction=signed_tx.rawTransaction)
        print(f'Transaction hash: {tx_hash.hex()}')
    except ValueError as VE:
        print(f'ERROR - value error')
        print(f'Code: {VE.args[0]["code"]}')
        print(f'Message: {VE.args[0]["message"]}')
        return (False, VE.args[0]["message"])
    except Exception as err:
        print(f"err: {err}")
        print(f"err.args: {err.args}")
        print(f"err.args: {err.args[0]}")
        return (True, err.args[0]["message"])

    try:
        tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash)
        print(f'Transaction receipt: {tx_receipt["transactionHash"].hex()}')
    except TimeExhausted as TE:
        print('ERROR - time exhausted')
        print(f'Code: {TE.args[0]["code"]}')
        print(f'Message: {TE.args[0]["message"]}')
        return (False, TE.args[0]["message"])
    except Exception as err:
        print(f"err: {err}")
        print(f"err.args: {err.args}")
        print(f"err.args: {err.args[0]}")
        return (True, err.args[0]["message"])

    return (True, tx_receipt)

def INCREASE_GAS(transaction: dict, percentage: float = app.config["GAS_INCREASE"]):
    transaction['maxFeePerGas'] = int((transaction['maxFeePerGas'] * \
        percentage) + transaction['maxFeePerGas'])
    transaction['maxPriorityFeePerGas'] = \
        int((transaction['maxPriorityFeePerGas'] * percentage) + \
        transaction['maxPriorityFeePerGas'])
    return transaction

def get_tx_pool_content(w3: Web3 = None):
    return w3.geth.txpool.content()

def get_tx_pool_status(w3: Web3 = None):
    return w3.geth.txpool.status()

def BASIC_TRANSACTION(w3: Web3 = None, address: str = None) -> dict:
    print(f"Gas price: {w3.fromWei(w3.eth.gas_price, 'gwei')}")
    print(f"Max Priority fee per gas: {w3.fromWei(w3.eth.max_priority_fee, 'gwei')}")
    print(f"From: {address}")
    print(f"Nonce: {w3.eth.get_transaction_count(address)}")

    return {
        'nonce': w3.eth.get_transaction_count(address),
        'from': address,
        'maxFeePerGas': w3.eth.gas_price, #w3.toWei(1, 'gwei'),
        'maxPriorityFeePerGas': w3.eth.max_priority_fee, # w3.toWei(1, 'gwei'),
    }

def eip55_address_check(addr):
    return Web3.toChecksumAddress(addr)