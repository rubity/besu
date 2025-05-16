import json
from web3 import Web3
from eth_account import Account

# === 1. Carregar chaves da conta e URL do nó ===
with open("../keys.json") as f:
    keys = json.load(f)

rpc_url = keys['besu']['rpcnode']['url']
private_key = "0x60bbe10a196a4e71451c0f6e9ec9beab454c2a5ac0542aa5b8b733ff5719fec3"
account = Account.from_key(private_key)

# === 2. Conectar ao nó ===
w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "Erro: Não conectado ao nó Ethereum"

# === 3. Carregar ABI e bytecode do contrato ===
with open("../../contracts/SimpleStorage.json") as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]
    bytecode = contract_json['evm']["bytecode"]['object']

# === 4. Criar contrato a partir do ABI e bytecode ===
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# === 5. Construir transação de deploy ===
nonce = w3.eth.get_transaction_count(account.address)
transaction = SimpleStorage.constructor(42).build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': w3.eth.gas_price,
})

# === 6. Assinar e enviar a transação ===
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
#signed_tx = Account.sign_transaction(transaction, private_key)
#print(type(signed_tx), signed_tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("Enviando contrato... hash da transação:", tx_hash.hex())

# === 7. Aguardar confirmação e obter endereço do contrato ===
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print("Contrato implantado em:", contract_address)

# === 8. Interagir com o contrato ===
contract = w3.eth.contract(address=contract_address, abi=abi)

# Chamar função `get()` (view)
valor = contract.functions.get().call()
print("Valor inicial armazenado:", valor)

# Chamar função `set()` (transação)
tx2 = contract.functions.set(99).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 100000,
    'gasPrice': w3.eth.gas_price,
})

signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key)
#signed_tx2 = Account.sign_transaction(tx2, private_key)
tx_hash2 = w3.eth.send_raw_transaction(signed_tx2.raw_transaction)
print("Enviando transação para set(99)...")

w3.eth.wait_for_transaction_receipt(tx_hash2)
valor2 = contract.functions.get().call()
print("Novo valor armazenado:", valor2)
