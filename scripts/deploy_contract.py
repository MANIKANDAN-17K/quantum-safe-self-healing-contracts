# scripts/deploy_contract.py

from web3 import Web3
from solcx import compile_source, install_solc
import json
import warnings
warnings.filterwarnings('ignore')

print("[Deploy] Installing Solidity compiler...")
install_solc('0.8.19')
print("[Deploy] Solidity compiler ready")

def deploy_contract():
    
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    
    if not w3.is_connected():
        print("[Deploy] ERROR: Ganache not running!")
        return None, None
    
    print(f"[Deploy] Connected to Ganache")
    print(f"[Deploy] Chain ID: {w3.eth.chain_id}")
    
    accounts = w3.eth.accounts
    owner = accounts[0]
    balance = w3.from_wei(w3.eth.get_balance(owner), 'ether')
    print(f"[Deploy] Owner: {owner}")
    print(f"[Deploy] Balance: {balance} ETH")
    
    with open('contracts/QuantumSafeContract.sol', 'r') as f:
        contract_source = f.read()
    
    print("[Deploy] Compiling contract...")
    compiled = compile_source(
        contract_source,
        output_values=['abi', 'bin'],
        solc_version='0.8.19'
    )
    
    contract_id = '<stdin>:QuantumSafeContract'
    contract_interface = compiled[contract_id]
    
    print("[Deploy] Deploying contract...")
    Contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    
    tx_hash = Contract.constructor().transact({
        'from': owner,
        'gas': 3000000
    })
    
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    
    print(f"[Deploy] Contract deployed!")
    print(f"[Deploy] Address: {contract_address}")
    
    contract_info = {
        'address': contract_address,
        'abi': contract_interface['abi'],
        'owner': owner,
        'accounts': accounts[:6]
    }
    
    with open('contract_info.json', 'w') as f:
        json.dump(contract_info, f, indent=2)
    
    print("[Deploy] Saved to contract_info.json")
    return w3, contract_info


if __name__ == "__main__":
    print("=" * 50)
    print("CONTRACT DEPLOYMENT")
    print("=" * 50)
    deploy_contract()