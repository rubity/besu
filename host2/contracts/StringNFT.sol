// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract StringNFT is ERC721, Ownable {
    uint256 private _nextTokenId;
    mapping(uint256 => string) private _tokenMessages;

    constructor() ERC721("StringNFT", "SNFT") Ownable(msg.sender) {}

    /// @notice Cria um novo NFT com uma mensagem associada
    function mint(address to, string memory mensagem) public onlyOwner returns (uint256) {
        uint256 tokenId = _nextTokenId;
        _safeMint(to, tokenId);
        _tokenMessages[tokenId] = mensagem;
        _nextTokenId++;
        return tokenId;
    }

    /// @notice Retorna a mensagem associada ao NFT
    function getMensagem(uint256 tokenId) public view returns (string memory) {
        _requireOwned(tokenId); // Garante que o token existe
        return _tokenMessages[tokenId];
    }
}

