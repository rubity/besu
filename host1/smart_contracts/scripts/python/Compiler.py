import json
from solcx import compile_standard, install_solc

# Instale o compilador Solidity 0.8.20 (apenas uma vez)
install_solc("0.8.20")

with open("/home/augusto/besu/smart_contracts/contracts/ecdsa/ecdsa_signature.sol", "r") as file:
    source_code = file.read()

compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "ecdsa.sol": {
                "content": source_code
            }
        },
        "settings": {
            "optimizer": {
                "enabled": True,
                "runs": 200
            },
            "viaIR": True,
            "remappings": [
                "@openzeppelin/=/home/augusto/besu/smart_contracts/node_modules/@openzeppelin/contracts/"
            ],
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.20",
)

# Salva em um arquivo para facilitar
with open("/home/augusto/besu/smart_contracts/contracts/ecdsa/ecdsa_signature.json", "w") as f:
    json.dump(compiled, f, indent=2)

print("✅ Compilação concluída com sucesso!")
