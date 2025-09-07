const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("Compiling contracts...");
  
  // Compile contracts first
  await hre.run("compile");
  
  console.log("Deploying AnchorChain contract...");
  
  // Wait for network to be ready
  let retries = 30;
  while (retries > 0) {
    try {
      await hre.ethers.provider.getNetwork();
      break;
    } catch (error) {
      console.log(`Waiting for network... (${retries} retries left)`);
      await new Promise(resolve => setTimeout(resolve, 2000));
      retries--;
    }
  }
  
  if (retries === 0) {
    throw new Error("Network not available");
  }

  const AnchorChain = await hre.ethers.getContractFactory("AnchorChain");
  const anchorChain = await AnchorChain.deploy();
  
  await anchorChain.waitForDeployment();
  
  const address = await anchorChain.getAddress();
  console.log("AnchorChain deployed to:", address);
  
  // Get ABI
  const artifact = await hre.artifacts.readArtifact("AnchorChain");
  
  // Save contract info to shared volume
  const contractInfo = {
    address: address,
    abi: artifact.abi,
    deployedAt: new Date().toISOString()
  };
  
  const outputDir = "/shared/anchor";
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  fs.writeFileSync(
    path.join(outputDir, "contract.json"),
    JSON.stringify(contractInfo, null, 2)
  );
  
  console.log("Contract info saved to /shared/anchor/contract.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
