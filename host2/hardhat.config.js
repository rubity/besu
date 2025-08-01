require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.28",
  networks: {
    besu: {
      url: "http://10.0.0.77:8545", // ou o IP/porta pública da sua Besu
      accounts: [ "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63" ]
    }
  }
};

