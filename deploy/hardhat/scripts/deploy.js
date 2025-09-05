const fs = require('fs');
const path = require('path');

async function main() {
  console.log("Deploying AnchorChain contract...");
  
  const AnchorChain = await ethers.getContractFactory("AnchorChain");
  const anchorChain = await AnchorChain.deploy();
  
  await anchorChain.waitForDeployment();
  
  const address = await anchorChain.getAddress();
  console.log("AnchorChain deployed to:", address);
  
  // Get ABI
  const artifact = await hre.artifacts.readArtifact("AnchorChain");
  
  // Write contract info to shared volume
  const contractInfo = {
    address: address,
    abi: artifact.abi
  };
  
  const outputDir = '/shared/anchor';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  fs.writeFileSync(
    path.join(outputDir, 'contract.json'),
    JSON.stringify(contractInfo, null, 2)
  );
  
  console.log("Contract info written to /shared/anchor/contract.json");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
