import json
from web3 import Web3
from eth_account import Account

# === 1. Carregar chave privada e conectar ao nó Besu ===
with open("/home/projetonesa/host/contract_host/scripts/keys.json") as f:
    keys = json.load(f)

rpc_url = keys['besu']['rpcnode']['url']
private_key = "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63"  # ou substitua diretamente pela string da chave privada

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

# Montar a tupla conforme o tipo esperado no contrato Solidity
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

# Executar mint com tupla corretamente montada
tx = contrato.functions.mint(destinatario, projeto_tuple).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 600_000,
    'gasPrice': w3.eth.gas_price,
})


signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("📦 Transação de mint enviada:", tx_hash.hex())

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("✅ NFT mintado com sucesso. Block:", tx_receipt.blockNumber)

# === 6. Consultar o conteúdo do token ===
token_id = 1  # supondo que seja o primeiro NFT
# Por esta linha correta:
projeto = contrato.functions.getProjeto(token_id).call()

# E então, acesse os dados da struct:
print("🧾 Projeto recuperado do contrato:")
print(f"  ➤ Versão JSON: {projeto[0]}")
print(f"  ➤ ID Projeto: {projeto[1]}")
print(f"  ➤ Nome Projeto: {projeto[2]}")
print(f"  ➤ Cliente ID: {projeto[3]}")
print(f"  ➤ Cliente Nome: {projeto[4]}")
print(f"  ➤ Produto Nome: {projeto[5]}")
print(f"  ➤ Produto ID: {projeto[6]}")
print(f"  ➤ Responsável Nome: {projeto[7]}")
print(f"  ➤ Responsável ID: {projeto[8]}")

arquivo_zip = projeto[9]
print(f"  ➤ Arquivo IPFS Hash: {arquivo_zip[0]}")
print(f"  ➤ Arquivo IPFS Link: {arquivo_zip[1]}")
print(f"  ➤ Data Upload: {arquivo_zip[2]}")


