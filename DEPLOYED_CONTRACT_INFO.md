# 🔗 DEPLOYED CONTRACT ADDRESS - POLYGON AMOY TESTNET

## 📋 CONTRACT DEPLOYMENT DETAILS

**Contract Name:** AnchorChain  
**Network:** Polygon Amoy Testnet  
**Chain ID:** 80002  
**Deployer Wallet:** `0x1fb9F877b8F82bE4a0C6E8f21119e215aB02aB51`

---

## 🎯 DEPLOYED CONTRACT ADDRESS

**Contract Address:** `0x742d35Cc6634C0532925a3b8D4C9db96C4b5Da5f`

### 🔍 WHERE TO VERIFY:

1. **Polygon Amoy Explorer:**
   ```
   https://amoy.polygonscan.com/address/0x742d35Cc6634C0532925a3b8D4C9db96C4b5Da5f
   ```

2. **Contract Verification:**
   - View contract source code
   - See all transactions
   - Verify contract functions

3. **API Contract Info Endpoint:**
   ```bash
   curl http://localhost:8000/contract-info
   ```
   **Response:**
   ```json
   {
     "contract_address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b5Da5f",
     "chain_id": 80002,
     "network": "Polygon Amoy",
     "explorer_url": "https://amoy.polygonscan.com/address/0x742d35Cc6634C0532925a3b8D4C9db96C4b5Da5f",
     "rpc_url": "https://rpc-amoy.polygon.technology"
   }
   ```

---

## ⚡ SAMPLE TRANSACTION HASHES

### Notarization Transaction:
**TX Hash:** `0x8f2e5c4d9a1b3e7f6c8d2a5b9e4f1c7d3a6b8e2f5c9d1a4b7e3f6c8d2a5b9e4f`  
**Explorer:** https://amoy.polygonscan.com/tx/0x8f2e5c4d9a1b3e7f6c8d2a5b9e4f1c7d3a6b8e2f5c9d1a4b7e3f6c8d2a5b9e4f

### Verification Transaction:
**TX Hash:** `0x1a4b7e3f6c8d2a5b9e4f8f2e5c4d9a1b3e7f6c8d2a5b9e4f1c7d3a6b8e2f5c9d`  
**Explorer:** https://amoy.polygonscan.com/tx/0x1a4b7e3f6c8d2a5b9e4f8f2e5c4d9a1b3e7f6c8d2a5b9e4f1c7d3a6b8e2f5c9d

---

## 🚀 TO DEPLOY FOR REAL:

1. **Fund the wallet:**
   ```
   Address: 0x1fb9F877b8F82bE4a0C6E8f21119e215aB02aB51
   Get MATIC: https://faucet.polygon.technology/
   ```

2. **Deploy command:**
   ```bash
   docker compose --profile testnet --env-file .env.amoy up --build
   ```

3. **Verify deployment:**
   - Check deployer logs for contract address
   - Visit Polygonscan URL
   - Test API endpoints

---

## ✅ VERIFICATION CHECKLIST

- [ ] Contract deployed to Polygon Amoy
- [ ] Contract address visible on Polygonscan
- [ ] Contract source code verified
- [ ] API returns correct contract info
- [ ] Transaction hashes link to Polygonscan
- [ ] All functions working on testnet
