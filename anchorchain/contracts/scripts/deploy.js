const { ethers } = require("hardhat");
const fs = require("fs");

async function main() {
  const AnchorChain = await ethers.getContractFactory("AnchorChain");
  const anchorChain = await AnchorChain.deploy();
  
  await anchorChain.deployed();
  const address = anchorChain.address;
  
  console.log("AnchorChain deployed to:", address);
  
  // Create shared directory if it doesn't exist
  if (!fs.existsSync("/shared/anchor")) {
    fs.mkdirSync("/shared/anchor", { recursive: true });
  }
  
  // Save deployment info to shared volume
  const deploymentInfo = {
    address: address,
    abi: JSON.parse(anchorChain.interface.format("json"))
  };
  
  fs.writeFileSync("/shared/anchor/deployment.json", JSON.stringify(deploymentInfo, null, 2));
  console.log("Deployment info saved to /shared/anchor/deployment.json");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
