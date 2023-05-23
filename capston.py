from web3 import Web3
from solcx import compile_standard, install_solc
import os
import json
from dotenv import load_dotenv

def compile_solidity():  
    load_dotenv()

    with open("./final_kickboard.sol", 'r', encoding = "UTF-8") as file:
        capston_file = file.read()

    install_solc("0.8.18")

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"final_kickboard.sol": {"content": capston_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                       "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.18",
    )

    with open("compiled_cap.json", "w") as file:
	    json.dump(compiled_sol, file)
            
    bytecode = compiled_sol["contracts"]["final_kickboard.sol"]["kickboard"]["evm"]["bytecode"]["object"]

    abi = json.loads(
        compiled_sol["contracts"]["final_kickboard.sol"]["kickboard"]["metadata"]
    )["output"]["abi"]

    return bytecode, abi

def make_CA(bytecode_cap, abi_cap):
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    chain_id = 1337
    my_address = "0x87dd65560773F050B06ec4954a68800E7223523A"
    private_key = os.getenv("PRIVATE_KEY")

    Capstonstorage = w3.eth.contract(abi=abi_cap, bytecode=bytecode_cap)

    nonce=w3.eth.get_transaction_count(my_address)

    Capston_tx = Capstonstorage.constructor('Hanyang', 20000, 'HYC').build_transaction({
        'from': my_address,
        'nonce': nonce,
        'gas': 3000000,
        'chainId': chain_id,
        'gasPrice': 1000000000,
    })

    # 스마트 컨트랙트 배포
    # # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(Capston_tx, private_key)
    # # # Send it!
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # # # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # print("CA: ",tx_receipt.contractAddress)
    return tx_receipt.contractAddress