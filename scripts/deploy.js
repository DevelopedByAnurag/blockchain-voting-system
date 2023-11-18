// scripts/deploy.js
const { ethers } = require("hardhat");

async function main() {
  // Load the VotingSmartContract contract factory
  const VotingSmartContract = await ethers.getContractFactory("VotingSmartContract");

  // Deploy the contract
  const votingContract = await VotingSmartContract.deploy(["Candidate1", "Candidate2"]); // Pass the candidate names as an array

  // Wait for the contract to be mined
  await votingContract.waitForDeployment();

  console.log("VotingSmartContract deployed to:", votingContract.target);
}

// Run the deployment function
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
