import json
from web3 import Web3

# Conectando ao nó Ethereum (local ou remoto)
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Conta padrão
w3.eth.default_account = w3.eth.accounts[0]  # ou use `w3.eth.account.privateKeyToAccount`

# Caminho para seu arquivo JSON gerado pelo compilador (ex: solc, Hardhat, Remix)
with open('SimpleStorage.json') as f:
    contract_json = json.load(f)

# ABI e Bytecode
abi = contract_json['abi']
# O bytecode pode estar em:
bytecode = contract_json.get('bytecode') or contract_json['evm']['bytecode']['object']

# Criando o contrato
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Enviando a transação para implantar (com parâmetro do construtor, ex: initVal=123)
tx_hash = SimpleStorage.constructor(123).transact()

# Espera a transação ser minerada
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Instância do contrato implantado
contract_instance = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Exemplo de chamada: ler valor armazenado
print("Stored value:", contract_instance.functions.get().call())
