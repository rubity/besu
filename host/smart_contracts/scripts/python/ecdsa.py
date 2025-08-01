import json
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

# === Configurações e conexão ===
with open("/home/augusto/besu/smart_contracts/scripts/keys.json") as f:
    keys = json.load(f)

rpc_url = keys['besu']['rpcnode']['url']
private_key = "0x60bbe10a196a4e71451c0f6e9ec9beab454c2a5ac0542aa5b8b733ff5719fec3"  # ou substitua manualmente
account = Account.from_key(private_key)

w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "❌ Erro: Não conectado ao nó"

# === Carregar ABI e endereço do contrato ===
with open("/home/augusto/besu/smart_contracts/contracts/ecdsa/ecdsa_signature.json") as f:
    contract_json = json.load(f)
    abi = contract_json['contracts']['ecdsa.sol']['RegistroDeDados']['abi']

contract_address = Web3.to_checksum_address("0xBca0fDc68d9b21b5bfB16D784389807017B2bbbc")
contract = w3.eth.contract(address=contract_address, abi=abi)

# === Carregar os dados do projeto JSON ===
with open("/home/augusto/besu/smart_contracts/scripts/python/mock.json") as f:
    dados = json.load(f)["projeto"]

# Conversões
def to_int1e6(val):
    return int(val * 1e6)

# Construindo os valores compatíveis com o Solidity
projeto_tuple = (
    dados["nome"],
    dados["codigo"],
    dados["ativo"],
    int(dados["orcamento"]),
    int(round((dados["orcamento"] % 1) * 100)),
    dados["numero_de_sensores"],
    int(dados["precisao_sensor"]),
    int(round((dados["precisao_sensor"] % 1) * 100)),
    dados["documentos"],
    (
        to_int1e6(dados["localizacao"]["latitude"]),
        to_int1e6(dados["localizacao"]["longitude"]),
    ),
    [
        (
            to_int1e6(p["latitude"]),
            to_int1e6(p["longitude"])
        )
        for p in dados["area_monitorada"]
    ],
    dados["descricao"]
)

# === Hash de mensagem ===
nonce = 42

msg_hash = Web3.solidity_keccak(
    [
        "string", "string", "bool", "uint256", "uint256",
        "uint256", "uint256", "uint256",
        "string", "string", "string",
        "int256", "int256",  # localizacao
        "int256", "int256",  # area[0]
        "int256", "int256",  # area[1]
        "int256", "int256",  # area[2]
        "int256", "int256",  # area[3]
        "string",
        "uint256", "address"
    ],
    [
        projeto_tuple[0],  # nome
        projeto_tuple[1],  # codigo
        projeto_tuple[2],  # ativo
        projeto_tuple[3],  # orcamentoInteiro
        projeto_tuple[4],  # orcamentoDecimal
        projeto_tuple[5],  # numeroDeSensores
        projeto_tuple[6],  # precisaoSensorInteiro
        projeto_tuple[7],  # precisaoSensorDecimal
        projeto_tuple[8][0],  # documentos[0]
        projeto_tuple[8][1],  # documentos[1]
        projeto_tuple[8][2],  # documentos[2]
        projeto_tuple[9][0],  # localizacao.latitude
        projeto_tuple[9][1],  # localizacao.longitude
        projeto_tuple[10][0][0],  # area[0].lat
        projeto_tuple[10][0][1],  # area[0].lng
        projeto_tuple[10][1][0],  # area[1].lat
        projeto_tuple[10][1][1],  # area[1].lng
        projeto_tuple[10][2][0],  # area[2].lat
        projeto_tuple[10][2][1],  # area[2].lng
        projeto_tuple[10][3][0],  # area[3].lat
        projeto_tuple[10][3][1],  # area[3].lng
        projeto_tuple[11],  # descricao
        nonce,
        contract_address
    ]
)

eth_msg = encode_defunct(hexstr=msg_hash.hex())
assinatura = Account.sign_message(eth_msg, private_key).signature

# === Enviar transação ===
tx = contract.functions.registrar(
    projeto_tuple,
    nonce,
    assinatura,
    account.address
).build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 2_000_000,
    "gasPrice": w3.eth.gas_price
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("✅ Transação enviada:", tx_hash.hex())
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("📦 Confirmada em bloco:", receipt.blockNumber)
