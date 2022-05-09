from solcx import compile_standard, install_solc
import json
from web3 import Web3
with open("./SimpleStorage.sol","r") as file:
    simple_storage_file = file.read()
    # We add these two lines that we forgot from the video!
    print("installing...")
    install_solc("0.8.10")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.10",
) 
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

#In case of local 
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id=1337
address = "...."
private_key = "0x622d739b956bcb8ebc4eae66c81f98865e3d4fb86bd7b3eefa60bb8839ba7c8e"


#In case of infura 
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/dc7d9f3df6fb4ec1a2ec29c80bc4e256"))
chain_id=4
address = "........"
private_key = "....."

print("Create the contract in Python")
# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print("get latest transaction")
# Get the latest transaction
nonce = w3.eth.getTransactionCount(address)
print(nonce)
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)


print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())
nonce = w3.eth.getTransactionCount(address)
print(nonce)
greeting_transaction1 = simple_storage.functions.store(30).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce ,
    }
)
signed_greeting_txn1 = w3.eth.account.sign_transaction(
    greeting_transaction1, private_key=private_key
)
tx_greeting_hash1 = w3.eth.send_raw_transaction(signed_greeting_txn1.rawTransaction)
print("Updating second time ")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash1)
print(simple_storage.functions.retrieve().call())