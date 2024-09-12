import sys
from web3 import Web3
import time
import random

infura_url = "https://rpc.ankr.com/bitlayer"
web3 = Web3(Web3.HTTPProvider(infura_url))

transactions = 10  # how many TXs will be send from each wallet
sleep_time = random.randint(5, 15)  # time between transactions


def generate_random_wallet():
    account = Web3().eth.account.create()
    return account.address


def generate_address_pairs(private_keys, transactions):
    address_pairs = []
    for pk in private_keys:
        for _ in range(transactions):
            recipient_address = generate_random_wallet()
            address_pairs.append(f"{pk}:{recipient_address}")
    return address_pairs


def tx_sender(private_key, recipient_address):
    if not web3.is_connected():
        raise Exception("Failed to connect to Ethereum network")

    account = (Web3().eth.account.from_key(private_key))
    address = account.address
    random_amount = round(random.uniform(0.000000001, 0.000000005), 11)
    nonce = web3.eth.get_transaction_count(address)

    tx = {
        'nonce': nonce,
        'to': recipient_address,
        'value': web3.to_wei(random_amount, 'ether'),
        'gas': 21000,
        'gasPrice': 50000010,
        'chainId': 200901
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt, address


with open('pks.txt', 'r') as file:
    private_keys = file.readlines()

private_keys = [pk.strip() for pk in private_keys]
keys_pairs = generate_address_pairs(private_keys, transactions)
random.shuffle(keys_pairs)

counter = 0
total_lines = len(keys_pairs)

for pair in keys_pairs:
    counter += 1

    private_key, recipient_address = pair.split(":")
    result = tx_sender(private_key, recipient_address)
    if result[0] is not None:
        print(f"Transaction has been sent from address: {result[1]} to {recipient_address} | hash: {result[0].transactionHash.hex()}")
        print(f'Sleep {sleep_time} sec')
        time.sleep(sleep_time)
    else:
        print("Error! Stop doing that shit")
        print(result)
        sys.exit()
