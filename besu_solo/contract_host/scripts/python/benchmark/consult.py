import json
import time
from web3 import Web3

# === Configuração da conexão ===
with open("../../keys.json") as f:
    keys = json.load(f)

rpc_url = keys['besu']['rpcnode']['url']
w3 = Web3(Web3.HTTPProvider(rpc_url))
assert w3.is_connected(), "❌ Erro: Não conectado ao nó"

# === Carregar ABI e endereço ===
with open("../../../contracts/benchmark/benchmark.json") as f:
    contract_json = json.load(f)
    abi = contract_json['contracts']['../../contracts/benchmark/benchmark.sol']['RegistroDeDadosSimplificado']['abi']

contract_address = Web3.to_checksum_address("0x6468751F5D94540338058254D8F9BD1AcEa498Fe")
contract = w3.eth.contract(address=contract_address, abi=abi)

# === Nonces usados para struct e json ===
nonce_struct = 55
nonce_json = 56

# === Consulta da struct ===
print(f"\n⏱ Consultando struct no nonce {nonce_struct}...")
try:
    start = time.time()
    projeto = contract.functions.projetosPorNonce(nonce_struct).call()
    end = time.time()
    print(f"✔️ Struct recuperada com sucesso em {end - start:.2f}s")
    print(f"📦 Dados da struct:\n{projeto}")
except Exception as e:
    print(f"❌ Erro ao consultar struct: {e}")

# === Consulta do JSON ===
print(f"\n⏱ Consultando JSON no nonce {nonce_json}...")
try:
    start = time.time()
    json_string = contract.functions.jsonsPorNonce(nonce_json).call()
    end = time.time()
    if not json_string:
        print("⚠️ Nenhum JSON encontrado nesse nonce.")
    else:
        print(f"✔️ JSON recuperado em {end - start:.2f}s")
        print(f"📦 JSON: {json_string}")
except Exception as e:
    print(f"❌ Erro ao consultar JSON: {e}")

