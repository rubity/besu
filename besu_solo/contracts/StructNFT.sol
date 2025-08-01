// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ProjetoNFT is ERC721, Ownable {
    uint256 private _nextTokenId;

    struct ArquivoZip {
        string ipfs_hash;
        string ipfs_link;
        string data_upload; // ou você pode usar uint256 com timestamps
    }

    struct Projeto {
        string json_version;
        string proj_id;
        string proj_nome;
        string cliente_id;
        string cliente_nome;
        string prod_nome;
        string prod_id;
        string responsavel_nome;
        string responsavel_id;
        ArquivoZip arquivo_zip_ipfs;
    }

    mapping(uint256 => Projeto) private _tokenProjetos;

    constructor() ERC721("ProjetoNFT", "PNFT") Ownable(msg.sender) {}

    /// @notice Cria um novo NFT com dados do projeto associados
    function mint(address to, Projeto memory projeto) public onlyOwner returns (uint256) {
        uint256 tokenId = _nextTokenId;
        _safeMint(to, tokenId);
        _tokenProjetos[tokenId] = projeto;
        _nextTokenId++;
        return tokenId;
    }

    /// @notice Retorna os dados do projeto associados ao NFT
    function getProjeto(uint256 tokenId) public view returns (Projeto memory) {
        _requireOwned(tokenId);
        return _tokenProjetos[tokenId];
    }
}

