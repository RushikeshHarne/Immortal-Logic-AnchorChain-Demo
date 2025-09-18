// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract AnchorChain {
    struct SoulState {
        bytes32 identityHash;
        bytes32 missionHash;
        uint256 timestamp;
        string jurisdiction;
        bool isActive;
    }

    struct ResurrectionEvent {
        string agentId;
        string sourceEmbodiment;
        string targetEmbodiment;
        bytes32 stateHash;
        uint256 timestamp;
    }

    mapping(address => SoulState[]) public soulStates;
    mapping(string => ResurrectionEvent[]) public resurrections;
    
    event SoulStateAnchored(address indexed entity, bytes32 identityHash, bytes32 missionHash);
    event ResurrectionRecorded(string indexed agentId, string sourceEmbodiment, string targetEmbodiment);

    function anchorSoulState(bytes32 _identityHash, bytes32 _missionHash, string memory _jurisdiction) external {
        soulStates[msg.sender].push(SoulState({
            identityHash: _identityHash,
            missionHash: _missionHash,
            timestamp: block.timestamp,
            jurisdiction: _jurisdiction,
            isActive: true
        }));
        
        emit SoulStateAnchored(msg.sender, _identityHash, _missionHash);
    }

    function recordResurrection(string memory _agentId, string memory _sourceEmbodiment, 
                              string memory _targetEmbodiment, bytes32 _identityHash, 
                              bytes32 _missionHash, string memory _jurisdiction) external {
        
        bytes32 stateHash = keccak256(abi.encodePacked(_identityHash, _missionHash, _jurisdiction));
        
        resurrections[_agentId].push(ResurrectionEvent({
            agentId: _agentId,
            sourceEmbodiment: _sourceEmbodiment,
            targetEmbodiment: _targetEmbodiment,
            stateHash: stateHash,
            timestamp: block.timestamp
        }));
        
        emit ResurrectionRecorded(_agentId, _sourceEmbodiment, _targetEmbodiment);
    }

    function getSoulState(address _entity, uint256 _index) external view returns (bytes32, bytes32, uint256, string memory, bool) {
        require(_index < soulStates[_entity].length, "Index out of bounds");
        SoulState memory state = soulStates[_entity][_index];
        return (state.identityHash, state.missionHash, state.timestamp, state.jurisdiction, state.isActive);
    }

    function getResurrectionCount(string memory _agentId) external view returns (uint256) {
        return resurrections[_agentId].length;
    }

    function getSoulStateCount(address _entity) external view returns (uint256) {
        return soulStates[_entity].length;
    }
}
