const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  
  console.log("Contract deployed with the account:", deployer.address);

  // Replace this with your deployed contract address
  const contractAddress = "0x42699A7612A82f1d9C36148af9C77354759b210b";
  
  // Replace this with the ABI of your contract
  const abi = [
    "event TripStored(uint256 tripId, address tripOwner, string distance, uint256 startTime, string startLocation, uint256 timestamp)",
    "function getTrip(uint256 _tripId) view returns (address tripOwner, string startLocation, string endLocation, string distance, string avgRPM, string avgSpeed, string avgEngLoad, uint256 startTime, uint256 endTime, uint256 timestamp)",
    "function storeTrip(string _startLocation, string _endLocation, string _distance, string _avgRPM, string _avgSpeed, string _avgEngLoad, uint256 _startTime, uint256 _endTime)",
    "function tripCounter() view returns (uint256)",
    "function trips(uint256) view returns (uint256 tripId, address tripOwner, string startLocation, string endLocation, string distance, string avgRPM, string avgSpeed, string avgEngLoad, uint256 startTime, uint256 endTime, uint256 timestamp)"
  ];
    // Create a contract instance
    const contract = new ethers.Contract(contractAddress, abi, deployer);

    // Send a transaction to store a new trip (write operation)
    try {
      const startLocation = "-5.843611, -35.199049";
      const endLocation = "-5.841978, -35.202699";
      const distance = "10";
      const avgRPM = "1300";
      const avgSpeed = "75"; // km
      const avgEngLoad = "49"; // m/s^2
      const startTime = 1730923208; // Electric car, no CO2 emissions
      const endTime = 1730923350; // 1 hour
  
      const tx = await contract.storeTrip(
        startLocation,
        endLocation,
        distance,
        avgRPM,
        avgSpeed,
        avgEngLoad,
        startTime,
        endTime
      );
      await tx.wait(); // Wait for the transaction to be mined
      console.log("Trip stored successfully.", tx.hash);
    } catch (error) {
      console.error("Error storing trip:", error);
    }

    // Call a function on the contract (read operation)
    const tripId = 0; // Example trip ID to retrieve
    try {
      const trip = await contract.getTrip(tripId);
      console.log("Trip details:", trip);
    } catch (error) {
      console.error("Error retrieving trip:", error);
    }
  }
  
main().catch(console.error);