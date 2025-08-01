import json
import time
from web3 import Web3
from eth_account import Account

# === 1. Carregar chave privada e conectar ao nó Besu ===
with open("/home/projetonesa/host/contract_host/scripts/keys.json") as f:
    keys = json.load(f)

rpc_url = keys['besu']['rpcnode']['url']
private_key = "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63"

account = Account.from_key(private_key)
w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "❌ Não conectado ao nó Ethereum"
print(f"✅ Conectado como {account.address}")

# === 2. Carregar ABI do contrato ===
with open("/home/projetonesa/host/artifacts/contracts/StructNFT.sol/ProjetoNFT.json") as f:
    contract_json = json.load(f)

abi = contract_json['abi']

# === 3. Endereço do contrato ===
contract_address = Web3.to_checksum_address("0xC9Bc439c8723c5c6fdbBE14E5fF3a1224f8A0f7C")
contrato = w3.eth.contract(address=contract_address, abi=abi)
print(f"✅ Contrato carregado em: {contract_address}")

# === 4. JSON de dados do projeto ===
json_projeto = {
    "projeto": {
        "json_version": "0.0.1",
        "proj_id": "7563458",
        "proj_nome": "Monitoramento Ambiental - Serra do Cipó",
        "cliente_id": "0896O",
        "cliente_nome": "Instituto Verde",
        "prod_nome": "Plano de Trabalho",
        "prod_id": "547563",
        "responsavel_nome": "Dra. Ana Silva",
        "responsavel_id": "574359",
        "arquivo_zip_ipfs": {
            "ipfs_hash": "QmX1y2Z3AbCdEfG...",
            "ipfs_link": "https://gateway.pinata.cloud/ipfs/QmX1y2Z3AbCdEfG...",
            "data_upload": "2025-06-10T14:30:00Z"
        }
    }
}

projeto = json_projeto["projeto"]
arquivo_ipfs = projeto["arquivo_zip_ipfs"]

# Montar tupla
projeto_tuple = (
    projeto["json_version"],
    projeto["proj_id"],
    projeto["proj_nome"],
    projeto["cliente_id"],
    projeto["cliente_nome"],
    projeto["prod_nome"],
    projeto["prod_id"],
    projeto["responsavel_nome"],
    projeto["responsavel_id"],
    (
        arquivo_ipfs["ipfs_hash"],
        arquivo_ipfs["ipfs_link"],
        arquivo_ipfs["data_upload"]
    )
)

destinatario = account.address
nonce = w3.eth.get_transaction_count(account.address)

# === 5. Executar benchmark ===
insertion_times = []
read_times = []

print("🚀 Iniciando benchmark (100 inserções e leituras)...")

for i in range(100):
    # Inserção
    start_insert = time.time()

    tx = contrato.functions.mint(destinatario, projeto_tuple).build_transaction({
        'from': account.address,
        'nonce': nonce + i,
        'gas': 600_000,
        'gasPrice': w3.eth.gas_price,
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    end_insert = time.time()
    insertion_times.append(end_insert - start_insert)

    token_id = receipt["logs"][0]["topics"][3] if len(receipt["logs"]) > 0 else i  # fallback
    token_id = int(token_id.hex(), 16) if isinstance(token_id, bytes) else i

    # Leitura
    start_read = time.time()
    projeto_lido = contrato.functions.getProjeto(token_id).call()
    end_read = time.time()
    read_times.append(end_read - start_read)

    print(f"🔁 {i+1}/100 - Token ID: {token_id} | Insert: {insertion_times[-1]:.2f}s | Read: {read_times[-1]:.2f}s")

# === 6. Resultados ===
avg_insert = sum(insertion_times) / len(insertion_times)
avg_read = sum(read_times) / len(read_times)
avg_total = avg_insert + avg_read

print("\n📊 Resultados médios após 100 execuções:")
print(f"⏱️ Tempo médio de inserção: {avg_insert:.2f} segundos")
print(f"📖 Tempo médio de leitura:   {avg_read:.2f} segundos")
print(f"🧮 Tempo total médio:        {avg_total:.2f} segundos")

