from solcx import compile_standard, install_solc
import json

# Instala o compilador solc 0.8.0, se ainda não estiver instalado
install_solc('0.8.10')

# Caminho para o contrato
solidity_file = "smart_contracts/contracts/SimpleStorage.sol"
output_file = "smart_contracts/contracts/SimpleStorage.json"

# Ler o código do contrato
with open(solidity_file, "r") as f:
    source_code = f.read()

# Compilar
compiled = compile_standard({
    "language": "Solidity",
    "sources": {
        solidity_file: {
            "content": source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, solc_version="0.8.10")

# Salvar resultado no JSON
with open(output_file, "w") as f:
    json.dump(compiled, f, indent=2)

print(f"Contrato compilado com sucesso! ABI e bytecode salvos em {output_file}")
