import json
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
#from eth_abi.packed import encode_abi_packed


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
with open("../../contracts/ecdsa/ecdsa_signature.json") as f:
    contract_json = json.load(f)
    abi = contract_json['contracts']['ecdsa.sol']['RegistroDeDados']["abi"]
    bytecode = contract_json['contracts']['ecdsa.sol']['RegistroDeDados']['evm']["bytecode"]['object']

# === 4. Criar contrato a partir do ABI e bytecode ===
RegistroDeDados = w3.eth.contract(abi=abi, bytecode=bytecode)

# === 5. Implantar o contrato ===
nonce = w3.eth.get_transaction_count(account.address)
tx = RegistroDeDados.constructor().build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': w3.eth.gas_price,
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("Deploy enviado, hash:", tx_hash.hex())

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print("Contrato implantado em:", contract_address)

# === 6. Interagir com o contrato ===
contract = w3.eth.contract(address=contract_address, abi=abi)

# === 7. Preparar mensagem, nonce e assinar ===
dado = "temperatura=28C"
nonce = 123
endereco_contrato = contract_address

# Criar o hash da mensagem (deve ser idêntico ao usado no Solidity)
msg_hash = Web3.solidity_keccak(
    ["string", "uint256", "address"],
    [dado, nonce, endereco_contrato]
)

# Adicionar prefixo Ethereum (personal_sign)
eth_msg = encode_defunct(hexstr=msg_hash.hex())

# Assinar mensagem
assinatura = Account.sign_message(eth_msg, private_key).signature

# === 8. Enviar a transação `registrar()` ===
tx2 = contract.functions.registrar(dado, nonce, assinatura, account.address).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price,
})

signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key)
tx_hash2 = w3.eth.send_raw_transaction(signed_tx2.raw_transaction)
print("Transação registrar() enviada:", tx_hash2.hex())

w3.eth.wait_for_transaction_receipt(tx_hash2)
print("✅ Transação confirmada.")
