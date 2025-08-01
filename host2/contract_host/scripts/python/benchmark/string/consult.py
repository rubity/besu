import json
import time
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

# === 3. Endereço do contrato ===
contract_address = Web3.to_checksum_address("0x42699A7612A82f1d9C36148af9C77354759b210b")
contrato = w3.eth.contract(address=contract_address, abi=abi)
print(f"✅ Contrato carregado em: {contract_address}")

# === 4. Loop para mintar e consultar NFTs ===
qtd_iteracoes = 10
tempo_mint_total = 0
tempo_consulta_total = 0
destinatario = account.address
nonce = w3.eth.get_transaction_count(account.address)

print("⏱️ Iniciando inserções...")

# === MINT ===
for i in range(qtd_iteracoes):
    mensagem = f"NFT {i+1} - teste de performance"
    
    tx = contrato.functions.mint(destinatario, mensagem).build_transaction({
        'from': account.address,
        'nonce': nonce + i,
        'gas': 300_000,
        'gasPrice': w3.eth.gas_price,
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    
    inicio = time.time()
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    fim = time.time()

    tempo_mint_total += (fim - inicio)

print("✅ Mint concluído.")

# === CONSULTA ===
print("⏱️ Iniciando consultas...")

for i in range(1, qtd_iteracoes + 1):  # IDs de 1 até 100, assumindo que tokenId começa em 1
    inicio = time.time()
    mensagem_lida = contrato.functions.getMensagem(i).call()
    fim = time.time()

    tempo_consulta_total += (fim - inicio)
    # print(f"ID {i}: {mensagem_lida}")

# === RESULTADOS ===
tempo_total = tempo_mint_total + tempo_consulta_total
print(f"\n📊 Resultados após {qtd_iteracoes} inserções e consultas:")
print(f"⛏️ Tempo médio de inserção (mint): {tempo_mint_total/qtd_iteracoes:.4f} s")
print(f"📖 Tempo médio de consulta (getMensagem): {tempo_consulta_total/qtd_iteracoes:.4f} s")
print(f"⏱️ Tempo total médio por par inserção+consulta: {tempo_total/qtd_iteracoes:.4f} s")

