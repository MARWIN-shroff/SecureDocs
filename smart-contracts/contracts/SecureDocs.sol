// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureDocs {
    mapping(bytes32 => bool) private documentHashes;
    mapping(bytes32 => address) private documentOwners;
    mapping(bytes32 => uint256) private documentTimestamps;
    
    event DocumentStored(bytes32 indexed documentHash, address indexed owner, uint256 timestamp);
    
    function storeDocument(bytes32 documentHash) public {
        require(!documentHashes[documentHash], "Document hash already exists");
        
        documentHashes[documentHash] = true;
        documentOwners[documentHash] = msg.sender;
        documentTimestamps[documentHash] = block.timestamp;
        
        emit DocumentStored(documentHash, msg.sender, block.timestamp);
    }
    
    function verifyDocument(bytes32 documentHash) public view returns (bool) {
        return documentHashes[documentHash];
    }
    
    function getDocumentInfo(bytes32 documentHash) public view returns (address owner, uint256 timestamp) {
        require(documentHashes[documentHash], "Document not found");
        return (documentOwners[documentHash], documentTimestamps[documentHash]);
    }
    
    function isOwner(bytes32 documentHash, address owner) public view returns (bool) {
        return documentOwners[documentHash] == owner;
    }
}
