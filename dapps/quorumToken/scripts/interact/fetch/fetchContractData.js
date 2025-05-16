const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  
  console.log("Interacting with the contract using the account:", deployer.address);

  // Replace this with your deployed contract address
  const contractAddress = "0x42699A7612A82f1d9C36148af9C77354759b210b";
  
  // Replace this with the ABI of your contract
  const abi = [
      
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "tripId",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "address",
          "name": "tripOwner",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "carModel",
          "type": "string"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "fuelType",
          "type": "string"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "distance",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "tripDuration",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "TripStored",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_tripId",
          "type": "uint256"
        }
      ],
      "name": "getTrip",
      "outputs": [
        {
          "internalType": "address",
          "name": "tripOwner",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "carModel",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "fuelType",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "initialLocation",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "finalLocation",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "distance",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "avgAcceleration",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "co2Emissions",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "tripStartTime",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "tripDuration",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_carModel",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_fuelType",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_initialLocation",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_finalLocation",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_distance",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_avgAcceleration",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_co2Emissions",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_tripStartTime",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_tripDuration",
          "type": "uint256"
        }
      ],
      "name": "storeTrip",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "tripCounter",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "trips",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "tripId",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "tripOwner",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "carModel",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "fuelType",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "initialLocation",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "finalLocation",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "distance",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "avgAcceleration",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "co2Emissions",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "tripStartTime",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "tripDuration",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ];

  // Create a contract instance
  const contract = new ethers.Contract(contractAddress, abi, deployer);

  // Call a function on the contract (read operation)
  const tripId = 9; // Example trip ID to retrieve
  try {
    const trip = await contract.getTrip(tripId);

    // Extract individual fields from the returned trip object
    const [
      tripOwner, 
      carModel, 
      fuelType, 
      initialLocation, 
      finalLocation, 
      distance, 
      avgAcceleration, 
      co2Emissions, 
      tripStartTime, 
      tripDuration, 
      timestamp
    ] = trip;

    // Log the trip details
    console.log("Trip details:");
    console.log("Owner:", tripOwner);
    console.log("Car Model:", carModel);
    console.log("Fuel Type:", fuelType);
    console.log("Initial Location:", initialLocation);
    console.log("Final Location:", finalLocation);
    console.log("Distance:", distance.toString(), "km");
    console.log("Average Acceleration:", avgAcceleration.toString(), "m/s^2");
    console.log("CO2 Emissions:", co2Emissions.toString(), "g");

    // Handle tripStartTime and timestamp
    console.log("Trip Start Time:", typeof tripStartTime === 'object' && 'toNumber' in tripStartTime
      ? new Date(tripStartTime.toNumber() * 1000).toLocaleString()
      : new Date(Number(tripStartTime) * 1000).toLocaleString());

    console.log("Trip Duration:", tripDuration.toString(), "seconds");

    console.log("Timestamp:", typeof timestamp === 'object' && 'toNumber' in timestamp
      ? new Date(timestamp.toNumber() * 1000).toLocaleString()
      : new Date(Number(timestamp) * 1000).toLocaleString());
  } catch (error) {
    console.error("Error retrieving trip:", error);
  }
}

main().catch(console.error);
