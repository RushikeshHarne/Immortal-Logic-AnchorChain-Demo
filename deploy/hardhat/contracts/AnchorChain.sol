// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract AnchorChain {
    struct SoulState {
        string soulId;
        string stateHash;
        uint256 timestamp;
        address anchor;
    }
    
    mapping(string => SoulState) public soulStates;
    
    event SoulStateAnchored(
        string indexed soulId,
        string stateHash,
        uint256 timestamp,
        address indexed anchor
    );
    
    function anchorSoulState(string memory soulId, string memory stateHash) public {
        soulStates[soulId] = SoulState({
            soulId: soulId,
            stateHash: stateHash,
            timestamp: block.timestamp,
            anchor: msg.sender
        });
        
        emit SoulStateAnchored(soulId, stateHash, block.timestamp, msg.sender);
    }
    
    function getSoulState(string memory soulId) public view returns (SoulState memory) {
        return soulStates[soulId];
    }
}
