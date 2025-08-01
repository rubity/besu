const { ethers } = require("hardhat");

async function main() {
  console.log("Connecting to the network...");

  const accounts = await ethers.getSigners();

  if (accounts.length === 0) {
    console.log("No accounts found on the network.");
    return;
  }

  console.log("Accounts available on the network:");
  for (let i = 0; i < accounts.length; i++) {
    const address = await accounts[i].getAddress();
    const balance = await ethers.provider.getBalance(address);
    console.log(`Account ${i + 1}: ${address}`);
    console.log(`Balance: ${balance} ETH\n`);
  }
}

// Run the script and handle errors
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("An error occurred:", error);
    process.exit(1);
  });
