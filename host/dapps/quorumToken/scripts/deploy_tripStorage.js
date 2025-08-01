const hre = require("hardhat");
const fs = require("fs/promises")

async function main() {
  //const initialSupply = ethers.parseEther('10000.0')
  const TripStorage  = await hre.ethers.getContractFactory("TripStorage");
  const tripStorage = await TripStorage.deploy();
  console.log("Contract deploy at: %s", await tripStorage.getAddress());

  await tripStorage.waitForDeployment();
  await writeDeploymentInfo(tripStorage, "contract.json");
}

async function writeDeploymentInfo(contract, filename=""){
  const data = {
    network : hre.network.name,
    contract : {
      address: await contract.getAddress(),
      signerAddress: await contract.runner.address,
      abi: await contract.interface.format(),
    }
  }

  const content = JSON.stringify(data, null, 2);
  await fs.writeFile(filename, content, {encoding: "utf-8"});
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error)
  process.exitCode = 1
})