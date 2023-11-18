// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingSmartContract {
    // Structure to represent a voter
    struct Voter {
        bool hasVoted;
    }

    // Structure to represent a candidate
    struct Candidate {
        string name;
        uint256 voteCount;
    }

    // Address of the election authority
    address public electionAuthority;

    // Mapping of addresses to voters
    mapping(address => Voter) public voters;

    // Array of candidates
    Candidate[] public candidates;

    // Event to be emitted when a vote is cast
    event Voted(address indexed voter, uint256 indexed candidateIndex);

    // Constructor to set the election authority and add candidates
    constructor(string[] memory candidateNames) {
        electionAuthority = msg.sender;

        // Add candidates to the election
        for (uint256 i = 0; i < candidateNames.length; i++) {
            candidates.push(Candidate({
                name: candidateNames[i],
                voteCount: 0
            }));
        }
    }

    // Modifier to ensure only the election authority can perform certain actions
    modifier onlyAuthority() {
        require(msg.sender == electionAuthority, "Only the election authority can call this function");
        _;
    }

    // Modifier to ensure the voter has not voted already
    modifier hasNotVoted() {
        require(!voters[msg.sender].hasVoted, "You have already voted");
        _;
    }

    // Function to cast a vote
    function vote(uint256 candidateIndex) external hasNotVoted {
        require(candidateIndex < candidates.length, "Invalid candidate index");

        // Mark the voter as having voted
        voters[msg.sender].hasVoted = true;

        // Increment the vote count for the chosen candidate
        candidates[candidateIndex].voteCount++;

        // Emit the Voted event
        emit Voted(msg.sender, candidateIndex);
    }

    // Function to get the total number of candidates
    function getCandidateCount() external view returns (uint256) {
        return candidates.length;
    }

    // Function to get the details of a specific candidate
    function getCandidate(uint256 candidateIndex) external view returns (string memory name, uint256 voteCount) {
        require(candidateIndex < candidates.length, "Invalid candidate index");
        return (candidates[candidateIndex].name, candidates[candidateIndex].voteCount);
    }

    // Function to get whether a voter has voted
    function hasVoterVoted(address voterAddress) external view returns (bool) {
        return voters[voterAddress].hasVoted;
    }

    // Function to get the total vote count for all candidates
    function getTotalVoteCount() external view returns (uint256) {
        uint256 totalVotes = 0;
        for (uint256 i = 0; i < candidates.length; i++) {
            totalVotes += candidates[i].voteCount;
        }
        return totalVotes;
    }
}
