// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract AnchorChain {
    struct SoulState {
        bytes32 hash;
        uint256 timestamp;
        string metadata;
    }

    mapping(address => SoulState[]) public soulStates;
    
    event SoulStateAnchored(address indexed entity, bytes32 hash, uint256 timestamp);

    function anchorSoulState(bytes32 _hash, string memory _metadata) external {
        soulStates[msg.sender].push(SoulState({
            hash: _hash,
            timestamp: block.timestamp,
            metadata: _metadata
        }));
        
        emit SoulStateAnchored(msg.sender, _hash, block.timestamp);
    }

    function getSoulStateCount(address _entity) external view returns (uint256) {
        return soulStates[_entity].length;
    }

    function getSoulState(address _entity, uint256 _index) external view returns (bytes32, uint256, string memory) {
        require(_index < soulStates[_entity].length, "Index out of bounds");
        SoulState memory state = soulStates[_entity][_index];
        return (state.hash, state.timestamp, state.metadata);
    }
}
