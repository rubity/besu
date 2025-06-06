// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract TripStorage {

    struct Trip{
        uint tripId;
        address tripOwner; // Endereço do usuário
        string startLocation;
        string endLocation;
        string distance; // Distância em km
        string avgRPM; // Aceleração média em m/s^2
        string avgSpeed;
        string avgEngLoad;
        uint256 startTime; 
        uint256 endTime;
        uint256 timestamp;// Timestamp do momento em que a viagem foi registrada
    }

    // Contador de ID das viagens
    uint public tripCounter;
    
    // Mapeamento para armazenar as viagens por ID
    mapping(uint => Trip) public trips;

    // Evento emitido quando uma viagem é armazenada
    event TripStored(uint tripId, address tripOwner, string distance, uint256 startTime, string startLocation, uint256 timestamp);

    // Custom Modifiers
    // Write a modifier to check if a trip exists
    modifier tripExists(uint _tripId){
        require(_tripId < tripCounter, "Trip does not exist.");
        _;
    }

    // Função para armazenar os dados da viagem na blockchain
    function storeTrip(string memory _startLocation, string memory _endLocation, string memory _distance, string memory _avgRPM, string memory _avgSpeed, string memory _avgEngLoad, uint256 _startTime, uint256 _endTime) public {

        // Armazena a nova viagem
        trips[tripCounter] = Trip({
            tripId: tripCounter,
            tripOwner: msg.sender,
            startLocation: _startLocation,
            endLocation: _endLocation,
            distance: _distance, 
            avgRPM: _avgRPM,
            avgSpeed: _avgSpeed,
            avgEngLoad: _avgEngLoad,
            startTime: _startTime,
            endTime: _endTime,
            timestamp: block.timestamp
        });

        // Emite um evento que a viagem foi armazenada
        emit TripStored(tripCounter, msg.sender, _distance, _startTime, _startLocation, block.timestamp);

        tripCounter++; // Incrementa o ID da viagem
    }

    // Função para obter os dados de uma viagem
    function getTrip(uint _tripId) public view tripExists(_tripId) returns (
            address tripOwner, 
            string memory startLocation, 
            string memory endLocation, 
            string memory distance,
            string memory avgRPM, 
            string memory avgSpeed, 
            string memory avgEngLoad,
            uint256 startTime,
            uint256 endTime,
            uint256 timestamp) {
        Trip memory trip = trips[_tripId];
        return (
            trip.tripOwner,
            trip.startLocation,
            trip.endLocation,
            trip.distance,
            trip.avgRPM,
            trip.avgSpeed,
            trip.avgEngLoad,
            trip.startTime,
            trip.endTime,
            trip.timestamp
        );
    }
}