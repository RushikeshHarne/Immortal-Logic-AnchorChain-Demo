// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AnchorChain {
    event ResurrectionRecorded(
        string agentId,
        string sourceId,
        string targetId,
        bytes32 identityHash,
        bytes32 missionHash,
        string jurisdiction,
        address indexed caller,
        uint256 blockTime
    );

    mapping(string => string) public latestEmbodiment; // agentId => embodimentId
    mapping(string => bool)   public validEmbodiment;  // embodimentId => anchored

    function recordResurrection(
        string memory agentId,
        string memory sourceId,
        string memory targetId,
        bytes32 identityHash,
        bytes32 missionHash,
        string memory jurisdiction
    ) public {
        latestEmbodiment[agentId] = targetId;
        validEmbodiment[targetId] = true;
        emit ResurrectionRecorded(agentId, sourceId, targetId, identityHash, missionHash, jurisdiction, msg.sender, block.timestamp);
    }

    function validateEmbodiment(string memory embodimentId) public view returns (bool) {
        return validEmbodiment[embodimentId];
    }
}
