import json
from web3 import Web3
from eth_account import Account

# === 1. Carregar chaves e RPC ===
with open("/home/augusto/besu/smart_contracts/scripts/keys.json") as f:
    keys = json.load(f)

rpc_url = keys['besu']['rpcnode']['url']
private_key = "0x60bbe10a196a4e71451c0f6e9ec9beab454c2a5ac0542aa5b8b733ff5719fec3"
account = Account.from_key(private_key)

# === 2. Conectar ao nó ===
w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "❌ Erro: Não conectado ao nó Ethereum"

# === 3. Carregar ABI e bytecode ===
with open("/home/augusto/besu/smart_contracts/contracts/ecdsa/ecdsa_signature.json") as f:
    contract_json = json.load(f)

abi = contract_json['contracts']['ecdsa.sol']['RegistroDeDados']['abi']
bytecode = contract_json['contracts']['ecdsa.sol']['RegistroDeDados']['evm']['bytecode']['object']

# === 4. Criar instância do contrato ===
Contrato = w3.eth.contract(abi=abi, bytecode=bytecode)

# === 5. Montar transação de deploy ===
nonce = w3.eth.get_transaction_count(account.address)

tx = Contrato.constructor().build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gas': 2_000_000,
    'gasPrice': w3.eth.gas_price,
})

# === 6. Assinar e enviar ===
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("🚀 Deploy enviado. TX hash:", tx_hash.hex())

# === 7. Aguardar confirmação ===
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("✅ Contrato implantado em:", receipt.contractAddress)
