import json
from web3 import Web3
from eth_account import Account

# === 1. Conectar ao nó Besu e carregar a chave privada ===
with open("/home/projetonesa/host/contract_host/scripts/keys.json") as f:
    keys = json.load(f)

rpc_url = keys['besu']['rpcnode']['url']
private_key = "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63"
account = Account.from_key(private_key)

w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "❌ Não conectado ao nó Ethereum"
print(f"✅ Conectado como {account.address}")

# === 2. Carregar apenas o ABI do contrato compilado ===
with open("/home/projetonesa/host/artifacts/contracts/StringNFT.sol/StringNFT.json") as f:
    contract_json = json.load(f)

abi = contract_json['abi']

# === 3. Endereço do contrato já implantado ===
contract_address = Web3.to_checksum_address("0x42699A7612A82f1d9C36148af9C77354759b210b")
contrato = w3.eth.contract(address=contract_address, abi=abi)
print(f"✅ Contrato carregado em: {contract_address}")

# === 4. Testar função mint (criar NFT com string) ===
mensagem = "Esse é o meu primeiro NFT com string personalizada 5."
destinatario = account.address  # ou outro endereço válido

tx = contrato.functions.mint(destinatario, mensagem).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 300_000,
    'gasPrice': w3.eth.gas_price,
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("🎨 Transação de mint enviada:", tx_hash.hex())

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("✅ NFT mintado com sucesso.")
#print(tx_receipt)

# === 5. Ler a mensagem armazenada no NFT ===
mensagem_lida = contrato.functions.getMensagem(1).call()
print(f"🧾 Mensagem lida do NFT: {mensagem_lida}")

