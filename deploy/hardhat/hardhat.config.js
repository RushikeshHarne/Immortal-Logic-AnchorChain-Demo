require("@nomicfoundation/hardhat-toolbox");

const RPC_URL = process.env.RPC_URL || "http://anvil:8545";
const PRIVATE_KEY = process.env.PRIVATE_KEY || "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";
const CHAIN_ID = parseInt(process.env.CHAIN_ID || "31337");

module.exports = {
  solidity: "0.8.19",
  networks: {
    local: {
      url: RPC_URL,
      accounts: [PRIVATE_KEY],
      chainId: CHAIN_ID
    }
  }
};
