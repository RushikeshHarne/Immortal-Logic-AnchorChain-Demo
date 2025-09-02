from fastapi import FastAPI
from pydantic import BaseModel
import os
from web3 import Web3
from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse

app = FastAPI(title="AnchorChain API", version="0.1.0")

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL","http://localhost:8545")))
CONTRACT_ADDRESS = os.getenv("ANCHORCHAIN_CONTRACT_ADDRESS")
ABI_PATH = os.getenv("ANCHORCHAIN_ABI_PATH","anchorchain/abi/AnchorChain.json")
FOUNDER_KEY = os.getenv("FOUNDER_PRIVATE_KEY")

AC_TX_OK = Counter("anchorchain_tx_success_total","ok tx")
AC_TX_ERR = Counter("anchorchain_tx_failed_total","failed tx")

class AnchorReq(BaseModel):
    agentId: str
    sourceEmbodimentId: str
    targetEmbodimentId: str
    identityHash: str
    missionHash: str
    jurisdiction: str

@app.post("/anchor")
def anchor(r: AnchorReq):
    try:
        with open(ABI_PATH,"r") as f:
            abi = f.read()
        contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
        acct = w3.eth.account.from_key(FOUNDER_KEY)
        tx = contract.functions.recordResurrection(
            r.agentId, r.sourceEmbodimentId, r.targetEmbodimentId,
            Web3.to_bytes(hexstr=r.identityHash),
            Web3.to_bytes(hexstr=r.missionHash),
            r.jurisdiction
        ).build_transaction({"from":acct.address, "nonce": w3.eth.get_transaction_count(acct.address)})
        signed = acct.sign_transaction(tx)
        txh = w3.eth.send_raw_transaction(signed.rawTransaction)
        AC_TX_OK.inc()
        return {"status":"ok","txHash": txh.hex()}
    except Exception as e:
        AC_TX_ERR.inc()
        return {"status":"error","detail": str(e)}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return PlainTextResponse(generate_latest(), media_type="text/plain")
