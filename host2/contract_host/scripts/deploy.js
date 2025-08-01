async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  const NFT = await ethers.getContractFactory("StringNFT");
  const nft = await NFT.deploy();

  await nft.waitForDeployment(); // EQUIVALENTE a .deployed() no Ethers v5

  console.log("StringNFT deployed at:", await nft.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

