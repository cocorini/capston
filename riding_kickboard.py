import json
import os
import serial
import time

from dotenv import load_dotenv
from solcx import compile_standard, install_solc
from web3 import Web3

# 유저 등록하기
def register(capstonstorage, user_address, private_key):
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    user1=capstonstorage.functions.register().build_transaction({
    'from': user_address,
    'gas': 84000,
    'gasPrice': 875000000,
    'nonce': 0,
    })
    # tx 배포
    tx(user1, private_key)

# tx 배포
def tx(build_transaction, private_key):
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    signed_txn = w3.eth.account.sign_transaction(build_transaction, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# parking함수
def parking(user_address, capstonstorage, private_key):
    input={
        'from': user_address,
        'gas': 4000000,
        'gasPrice': 875000000,
        'nonce': 0,
    }
    add_cnt = capstonstorage.functions.addCnt().build_transaction(input)
    tx(add_cnt, private_key)

    # 아두이노: parameter값을 반환하거나 정해주는 함수를 부르는 과정이 필요함
    # 기준값에 따라 불값으로 변환해주는 과정이 필요함
    tilt_value = aduino()
    tilt_para = -1
    if tilt_value>=150 and tilt_value<=270:
        tilt_para = 1
    
    print('tilt값은:', tilt_para, '\n')

    trust_value = capstonstorage.functions.trustValue(+3, tilt_para*3).build_transaction(input)
    tx(trust_value, private_key)

    black_list = capstonstorage.functions.blacklist().build_transaction(input)
    tx(black_list, private_key)

    incentive = capstonstorage.functions.incentive().build_transaction(input)
    tx(incentive, private_key)

# 매번 결과상황 출력
def result(user_address, capstonstorage):
    input_from={
        'from': user_address,
    }

    ResultStr = ''
    isBlack, isUser = check_init(user_address, capstonstorage)

    ResultStr = "user 여부: " + str(isUser) + '\n'

    cnt = capstonstorage.functions.cnt_list(user_address).call(input_from)
    ResultStr = ResultStr + "user의 킥보드 이용횟수: " + str(cnt) + ' 회\n'

    trust = capstonstorage.functions.trust_value(user_address).call(input_from)
    ResultStr = ResultStr + "user의 신뢰점수: " + str(trust) + ' 점\n'

    balance = capstonstorage.functions.balance(user_address).call(input_from)
    ResultStr = ResultStr + "user의 토큰 잔액: " + str(balance) + " HYC\n"

    ResultStr = ResultStr + "user의 블랙리스트 포함 여부: " + str(isBlack) + '\n'

    print(ResultStr)
    return ResultStr

def check_init(user_address, capstonstorage):
    input_from={
        'from': user_address,
    }
    isblack = capstonstorage.functions.black_list(user_address).call(input_from)
    isuser = capstonstorage.functions.isUser(user_address).call(input_from)
    
    return isblack, isuser

# 아두이노 실행 함수
def aduino():
    py_serial=serial.Serial(
        port='COM3',
        baudrate=38400,
    )
    while True:
        if py_serial.readable():
            response = py_serial.readline()
            ready = response.decode()[:len(response)-1]
            print(ready)
        return float(ready)

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
    abi = json.loads(compiled_sol["contracts"]["final_kickboard.sol"]["kickboard"]["metadata"])["output"]["abi"]

    return bytecode, abi


def contract_inform(bytecode_cap, abi_cap, CA):
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    chain_id = 1337
    contract_address = CA

    capstonstorage = w3.eth.contract(
        address=contract_address,
        abi=abi_cap,
        bytecode=bytecode_cap,
    )
    return capstonstorage