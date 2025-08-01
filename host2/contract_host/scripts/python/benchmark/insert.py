import json
import time
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

# === Configurações ===
with open("../../keys.json") as f:
    keys = json.load(f)

rpc_url = keys['besu']['rpcnode']['url']
private_key = "0x60bbe10a196a4e71451c0f6e9ec9beab454c2a5ac0542aa5b8b733ff5719fec3"
account = Account.from_key(private_key)

w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "❌ Erro: Não conectado ao nó"

# === Carregar contrato ===
with open("../../../contracts/benchmark/benchmark.json") as f:
    contract_json = json.load(f)
    abi = contract_json['contracts']['../../contracts/benchmark/benchmark.sol']['RegistroDeDadosSimplificado']['abi']

contract_address = Web3.to_checksum_address("0x6410E8e6321f46B7A34B9Ea9649a4c84563d8045")  # seu contrato
contract = w3.eth.contract(address=contract_address, abi=abi)

# === Carregar dados do JSON ===
with open("../../BesuJSON.json") as f:
    dados = json.load(f)["projeto"]

# === Montar struct projeto como tupla ===
arquivo_zip_tuple = (
    dados["arquivo_zip_ipfs"]["ipfs_hash"],
    dados["arquivo_zip_ipfs"]["ipfs_link"],
    dados["arquivo_zip_ipfs"]["data_upload"]
)

projeto_tuple = (
    dados["json_vcontract_addressersion"],
    dados["proj_id"],
    dados["proj_nome"],
    dados["cliente_id"],
    dados["cliente_nome"],
    dados["prod_nome"],
    dados["prod_id"],
    dados["responsavel_nome"],
    dados["responsavel_id"],
    arquivo_zip_tuple
)

# === Nonces distintos ===
nonce_struct = 71
nonce_json = 72

# === Verificação prévia se já existe no contrato ===
try:
    dados_struct = contract.functions.projetosPorNonce(nonce_struct).call()
    if any(dados_struct):  # verifica se há algum valor não vazio na tupla
        print(f"⚠️ Struct já registrada para nonce {nonce_struct}, escolha outro.")
        exit()
except Exception as e:
    print(f"ℹ️ Nenhuma struct registrada para nonce {nonce_struct}, prosseguindo...")

try:
    dados_json = contract.functions.jsonsPorNonce(nonce_json).call()
    if dados_json != '':
        print(f"⚠️ JSON já registrado para nonce {nonce_json}, escolha outro.")
        exit()
except Exception as e:
    print(f"ℹ️ Nenhum JSON registrado para nonce {nonce_json}, prosseguindo...")


# === EncodePacked manual ===
def encode_packed_strings(*args):
    return "".join(args).encode("utf-8")

# === Assinatura para struct ===
packed_struct = encode_packed_strings(
    dados["json_version"],
    dados["proj_id"],
    dados["proj_nome"],
    dados["cliente_id"],
    dados["cliente_nome"],
    dados["prod_nome"],
    dados["prod_id"],
    dados["responsavel_nome"],
    dados["responsavel_id"],
    dados["arquivo_zip_ipfs"]["ipfs_hash"],
    dados["arquivo_zip_ipfs"]["ipfs_link"],
    dados["arquivo_zip_ipfs"]["data_upload"],
    str(nonce_struct)
)
msg_hash_struct = Web3.keccak(packed_struct)
eth_msg_struct = encode_defunct(hexstr=msg_hash_struct.hex())
assinatura_struct = Account.sign_message(eth_msg_struct, private_key).signature

# === Assinatura para JSON ===
json_string = json.dumps(dados)
#packed_json = encode_packed_strings(json_string, str(nonce_json))

# Criar o hash da mensagem (deve ser idêntico ao usado no Solidity)
msg_hash_json = Web3.solidity_keccak(
    ["string", "uint256", "address"],
    [json_string, nonce_json, contract_address]
)

#msg_hash_json = Web3.keccak(packed_json)
eth_msg_json = encode_defunct(hexstr=msg_hash_json.hex())
assinatura_json = Account.sign_message(eth_msg_json, private_key).signature

# === Função auxiliar para envio de transações ===
def enviar_transacao(func, *args):
    nonce_tx = w3.eth.get_transaction_count(account.address)
    tx = func(*args).build_transaction({
        "from": account.address,
        "nonce": nonce_tx,
        "gas": 999_000_000,
        "gasPrice": w3.eth.gas_price
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    start = time.time()
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(receipt)
    
    # Percorrer os logs para encontrar DebugHash
    for log in receipt.logs:
    # Usar a ABI do evento DebugHash para decodificar
        try:
            decoded_event = contract.events.DebugHash().processLog(log)
            print("DebugHash emitido:", decoded_event['args']['mensagemHash'].hex())
        except:
        # Esse log não é do DebugHash, ignorar
            pass

    
    end = time.time()

    if receipt["status"] == 1:
        print(f"✅ Transação confirmada em bloco {receipt['blockNumber']}")
    else:
        print("❌ Falha na transação")

    return receipt["blockNumber"], end - start, receipt

# === Inserção via STRUCT ===
print("⏱ Teste com struct...")

try:
    bloco_struct, tempo_struct, receipt_struct = enviar_transacao(
        contract.functions.registrar,
        projeto_tuple,
        nonce_struct,
        assinatura_struct,
        account.address
    )
except Exception as e:
    print(e)

# === Inserção via STRING JSON ===
print("⏱ Teste com string JSON...")
bloco_json, tempo_json, receipt_json = enviar_transacao(
    contract.functions.registrarJson,
    json_string,
    nonce_json,
    assinatura_json,
    account.address
)

# === Resultados ===
print(f"\n📊 Resultados:")
print(f"✔️ Struct: {tempo_struct:.2f}s no bloco {bloco_struct}")
print(f"✔️ JSON:   {tempo_json:.2f}s no bloco {bloco_json}")

from web3.exceptions import ContractLogicError

try:
    contract.functions.registrarJson(
        '{"teste": "ok"}',
        88,
        assinatura_json,
        account.address
    ).call({'from': account.address})
except Exception as e:
    print("Erro em call:", e)



