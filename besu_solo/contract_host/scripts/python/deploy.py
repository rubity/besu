from solcx import compile_standard, install_solc
from web3 import Web3
import json

# 1. Compile o contrato (supondo que você já tenha o source)
install_solc('0.8.20')

# === Configurações ===
with open("../keys.json") as f:
    keys = json.load(f)
    
# === Carregar contrato ===
with open("/home/projetonesa/host/contract_host/contracts/benchmark/string/string.json") as f:
    contract_json = json.load(f)
    abi = contract_json['contracts']['../../contracts/benchmark/string/string.sol']['StringNFT']['abi']
    bytecode = contract_json['contracts']['../../contracts/benchmark/string/string.sol']['StringNFT']['evm']['bytecode']['object']

# 2. Conectar ao nó
rpc_url = keys['besu']['rpcnode']['url']
private_key = "0x60bbe10a196a4e71451c0f6e9ec9beab454c2a5ac0542aa5b8b733ff5719fec3"
w3 = Web3(Web3.HTTPProvider(rpc_url))
account = w3.eth.account.from_key(private_key)
nonce = w3.eth.get_transaction_count(account.address)

# 3. Criar contrato
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# 4. Construir transação de deploy
tx = contract.constructor().build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gas': 3000000000,
    'gasPrice': w3.eth.gas_price
})

# 5. Assinar e enviar
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("Deploy tx hash:", tx_hash.hex())

# 6. Esperar a confirmação
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contrato implantado no endereço:", tx_receipt.contractAddress)

print(tx_receipt)

