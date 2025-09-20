// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract AnchorChain {
    struct ResurrectionRecord {
        bytes32 soulHash;
        uint256 timestamp;
        address notarizer;
        bool verified;
    }
    
    mapping(bytes32 => ResurrectionRecord) public records;
    mapping(address => uint256) public gasSpent;
    
    event ResurrectionNotarized(bytes32 indexed soulHash, address indexed notarizer, uint256 timestamp);
    event ResurrectionVerified(bytes32 indexed soulHash, bool success);
    
    function notarizeResurrection(bytes32 _soulHash) external {
        uint256 gasStart = gasleft();
        
        records[_soulHash] = ResurrectionRecord({
            soulHash: _soulHash,
            timestamp: block.timestamp,
            notarizer: msg.sender,
            verified: false
        });
        
        gasSpent[msg.sender] += gasStart - gasleft();
        emit ResurrectionNotarized(_soulHash, msg.sender, block.timestamp);
    }
    
    function verifyResurrection(bytes32 _soulHash) external returns (bool) {
        ResurrectionRecord storage record = records[_soulHash];
        require(record.timestamp > 0, "Record not found");
        
        record.verified = true;
        emit ResurrectionVerified(_soulHash, true);
        return true;
    }
    
    function getRecord(bytes32 _soulHash) external view returns (ResurrectionRecord memory) {
        return records[_soulHash];
    }
}
