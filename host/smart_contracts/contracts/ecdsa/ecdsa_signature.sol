// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";

contract RegistroDeDados {
    using MessageHashUtils for bytes32;
    using ECDSA for bytes32;

    address public dono;
    mapping(address => mapping(uint256 => bool)) public nonceUsado;

    struct Localizacao {
        int256 latitude;    // armazenar latitude e longitude em inteiros * 1e6 para evitar float
        int256 longitude;
    }

    struct AreaMonitorada {
        int256 latitude;
        int256 longitude;
    }

    struct Projeto {
        string nome;
        string codigo;
        bool ativo;
        uint256 orcamentoInteiro;
        uint256 orcamentoDecimal;  // separar parte decimal para simular float
        uint256 numeroDeSensores;
        uint256 precisaoSensorInteiro;
        uint256 precisaoSensorDecimal;
        string[3] documentos;
        Localizacao localizacao;
        AreaMonitorada[4] areaMonitorada;
        string descricao;
    }

    event ProjetoRegistrado(address remetente, Projeto projeto, uint256 nonce);

    constructor() {
        dono = msg.sender;
    }

    function registrar(
        Projeto memory projeto,
        uint256 nonce,
        bytes memory assinatura,
        address remetente
    ) public {
        require(!nonceUsado[remetente][nonce], "Nonce ja usado");

        // Criar hash da mensagem de acordo com todos os campos do projeto + nonce + endereço contrato
        bytes32 mensagemHash = keccak256(abi.encode(
            projeto.nome,
            projeto.codigo,
            projeto.ativo,
            projeto.orcamentoInteiro,
            projeto.orcamentoDecimal,
            projeto.numeroDeSensores,
            projeto.precisaoSensorInteiro,
            projeto.precisaoSensorDecimal,
            projeto.documentos[0],
            projeto.documentos[1],
            projeto.documentos[2],
            projeto.localizacao.latitude,
            projeto.localizacao.longitude,
            projeto.areaMonitorada[0].latitude,
            projeto.areaMonitorada[0].longitude,
            projeto.areaMonitorada[1].latitude,
            projeto.areaMonitorada[1].longitude,
            projeto.areaMonitorada[2].latitude,
            projeto.areaMonitorada[2].longitude,
            projeto.areaMonitorada[3].latitude,
            projeto.areaMonitorada[3].longitude,
            projeto.descricao,
            nonce,
            address(this)
        ));
        bytes32 hashComPrefixo = mensagemHash.toEthSignedMessageHash();

        address recuperado = hashComPrefixo.recover(assinatura);
        require(recuperado == remetente, "Assinatura invalida");

        nonceUsado[remetente][nonce] = true;

        emit ProjetoRegistrado(remetente, projeto, nonce);
    }
}

