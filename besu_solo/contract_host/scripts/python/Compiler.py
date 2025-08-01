from solcx import compile_standard, install_solc
import json, os

# Instala o compilador solc 0.8.20, se ainda não estiver instalado
install_solc('0.8.20')

# Caminho para o contrato
solidity_file = "../../contracts/Counter.sol"
output_file = "../../contracts/Counter.json"


# Caminho absoluto da raiz do projeto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Ler o código do contrato
with open(solidity_file, "r") as f:
    source_code = f.read()

# Compilar com viaIR ativado
compiled = compile_standard({
    "language": "Solidity",
    "sources": {
        solidity_file: {
            "content": source_code
        }
    },
    "settings": {
        "optimizer": {
            "enabled": False,
            "runs": 200
        },
        "viaIR": False,
        "remappings": [
            "@openzeppelin/=" + os.path.join(project_root, "node_modules/@openzeppelin/contracts/")
        ],
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, 
solc_version="0.8.20",
allow_paths=project_root
)

# Salvar resultado no JSON
with open(output_file, "w") as f:
    json.dump(compiled, f, indent=2)

print(f"Contrato compilado com sucesso com viaIR! ABI e bytecode salvos em {output_file}")

