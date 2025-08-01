const hre = require("hardhat");

async function main() {
  // Recupera a conta usada para o deploy
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying with account:", deployer.address);

  // Compila e instancia o contrato
  const ProjetoNFT = await hre.ethers.getContractFactory("ProjetoNFT");
  const contrato = await ProjetoNFT.deploy();

  await contrato.waitForDeployment();

  console.log("Contrato ProjetoNFT implantado em:", await contrato.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Erro ao implantar:", error);
    process.exit(1);
  });

