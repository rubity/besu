// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";

contract RegistroDeDados {
    using MessageHashUtils for bytes32;
    using ECDSA for bytes32;

    address public dono;
    mapping(address => mapping(uint256 => bool)) public nonceUsado;

    event DadoRegistrado(address remetente, string dado, uint256 nonce);

    constructor() {
        dono = msg.sender;
    }

    function registrar(
        string memory dado,
        uint256 nonce,
        bytes memory assinatura,
        address remetente
    ) public {
        require(!nonceUsado[remetente][nonce], "Nonce ja usado");

        // Recria o hash da mensagem original
        bytes32 mensagemHash = keccak256(abi.encodePacked(dado, nonce, address(this)));
        bytes32 hashComPrefixo = mensagemHash.toEthSignedMessageHash();

        // Recupera o signatário
        address recuperado = hashComPrefixo.recover(assinatura);
        require(recuperado == remetente, "Assinatura invalida");

        // Marca nonce como usado
        nonceUsado[remetente][nonce] = true;

        emit DadoRegistrado(remetente, dado, nonce);
    }
}
