import json
import random
import time

from web3 import *


f = open('data\\chains.json', 'r')
chains = json.loads(f.read())
f.close()


f = open('data\\erc_1155_abi.json', 'r')
erc_1155_abi = json.loads(f.read())
f.close()


f = open('data\\erc_721_abi.json', 'r')
erc_721_abi = json.loads(f.read())
f.close()


f = open('data\\erc20_token_abi.json', 'r')
erc20_token_abi = json.loads(f.read())
f.close()


def decimal_to_int(qty, decimal):
    return qty / pow(10, decimal)


def int_to_decimal(qty, decimal):
    return int(qty * pow(10, decimal))


def get_address(key):
    web3 = Web3(Web3.HTTPProvider(chains['ethereum']['rpc']))
    return web3.eth.account.from_key(key).address


def get_balance(key, chain, address_contract):
    try:
        web3 = Web3(Web3.HTTPProvider(chains[chain]['rpc']))
        checksum_address = web3.to_checksum_address(get_address(key))
        if address_contract == '':  # chain native token
            balance = web3.eth.get_balance(checksum_address)
            token_decimal = 18
            symbol = 'native'
        else:
            token_contract = web3.eth.contract(address=Web3.to_checksum_address(address_contract), abi=erc20_token_abi)
            token_decimal = token_contract.functions.decimals().call()
            symbol = token_contract.functions.symbol().call()
            balance = token_contract.functions.balanceOf(checksum_address).call()

        return symbol, balance, token_decimal

    except Exception as error:
        time.sleep(1)
        get_balance(key, chain, address_contract)


def check_allowance(w3, token_contract, owner_address, spender_address):
    try:
        return token_contract.functions.allowance(w3.to_checksum_address(owner_address), w3.to_checksum_address(spender_address)).call()
    except Exception as error:
        print(error)
        time.sleep(random.uniform(3, 10))
        check_allowance(token_contract, owner_address, spender_address)


def sign_tx(contract_txn, w3, key):
    signed_tx = w3.eth.account.sign_transaction(contract_txn, key)
    raw_tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = w3.to_hex(raw_tx_hash)

    while True:
        try:
            status = w3.eth.get_transaction_receipt(tx_hash)["status"]
            if status in [0, 1]:
                return status
            time.sleep(1)
        except Exception as error:
            print(error)
            time.sleep(1)


def approve_token_spending(w3, token_contract, owner_address, spender_address, key):
    try:
        print('approving')
        contract_txn = token_contract.functions.approve(
            w3.to_checksum_address(spender_address),
            115792089237316195423570985008687907853269984665640564039457584007913129639935
        ).build_transaction(
            {
                "chainId": w3.eth.chain_id,
                "from": w3.to_checksum_address(owner_address),
                "nonce": w3.eth.get_transaction_count(w3.to_checksum_address(owner_address)),
                'gasPrice': 0,
                'gas': 0,
                "value": 0
            }
        )

        if w3.eth.chain_id == 'bsc': #fixme specify bsc chain id
            contract_txn['gasPrice'] = random.randint(1000000000, 1050000000)  # специально ставим 1 гвей, так транза будет дешевле
        else:
            contract_txn['gasPrice'] = int(w3.eth.gas_price * random.uniform(1.01, 1.02))
        gas_limit = w3.eth.estimate_gas(contract_txn)
        contract_txn['gas'] = int(gas_limit * random.uniform(1.02, 1.05))

        status = sign_tx(contract_txn, w3, key)

        if status == 1:
            print('approved')
            time.sleep(random.uniform(5, 10))
            return True
        else:
            print('not approved')
            return False

    except Exception as error:
        print(error)
        return False


def wait_for_gas(w3, max_gas_price):
    while True:
        gas_price = w3.from_wei(w3.eth.gas_price, 'gwei')
        print('Current gas price: {}', gas_price)

        if gas_price < max_gas_price:
            break
        time.sleep(5)
