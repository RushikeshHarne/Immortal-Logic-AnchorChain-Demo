> Path: `docs/DEPLOYMENT_GUIDE.md`
> (On GitHub: **Add file → Create new file** → enter the path above → paste all of this → Commit.)

---

````markdown
# Immortal Logic System™ — Deployment Guide

This guide walks you through running the Immortal Logic System (ILS) locally (Docker Compose), optionally deploying **AnchorChain™** on testnet, and launching on **Kubernetes** with basic monitoring. Windows and macOS/Linux commands are both shown.

---

## 0) Prerequisites

- **Git**, **Docker Desktop** (with Compose), and (optional) **kubectl** + **Minikube**  
- **Python 3.10+** (for SDK and drills)  
- (Optional, for on-chain demo) An Ethereum/Polygon testnet RPC URL (Infura/Alchemy/etc.) and a funded test wallet (e.g., Sepolia ETH)

---

## 1) Clone & SDK quick check

```bash
git clone https://github.com/Nova1000x/immortal-logic.git
cd immortal-logic
````

Create and activate a virtual environment:

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r sdk/requirements.txt
```

**macOS/Linux (bash/zsh)**

```bash
python -m venv venv
source venv/bin/activate
pip install -r sdk/requirements.txt
```

Run the local resurrection drill (no blockchain):

```bash
python sdk/drills/epls_demo.py --mode=local
```

You should see logs like: `seal soul-state -> resurrect -> verify`.

---

## 2) Configure environment (.env)

Copy the example and edit:

```bash
cp .env.example .env
```

Required keys (leave blank if not using on-chain):

```
# General
ENV=dev

# AnchorChain API (Docker container will read these)
ANCHORCHAIN_PORT=8546

# Optional: EVM deployment (Sepolia recommended)
RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
WALLET_PRIVATE_KEY=0xYOUR_TEST_PRIVATE_KEY   # test wallet only
CHAIN_ID=11155111                            # 11155111 = Sepolia
```

> **Safety**: never commit `.env` to Git. It’s in `.gitignore` already.

---

## 3) Run the local stack (Docker Compose)

From repo root:

```bash
docker compose -f deploy/docker-compose.yml up --build
```

This brings up:

* `anchorchain-api` — the AnchorChain Python API
* (placeholders for) Prometheus/Grafana if enabled in your compose file

Check logs:

```bash
docker compose logs -f anchorchain-api
```

Stop:

```bash
docker compose down
```

---

## 4) (Optional) Deploy AnchorChain™ on testnet

> This step is optional. It notarizes resurrection events on-chain for the **onchain** drill mode.

1. Ensure `.env` has `RPC_URL`, `WALLET_PRIVATE_KEY`, `CHAIN_ID`.

2. (If you have a Hardhat/Foundry script later) For now, use the provided Python deploy script (placeholder) or a standard EVM deployment tool. Example placeholder:

```bash
# Inside anchorchain/ (future deploy tooling)
# python scripts/deploy_anchorchain.py --rpc $RPC_URL --pk $WALLET_PRIVATE_KEY
```

3. Put the deployed contract address into `.env`:

```
ANCHORCHAIN_CONTRACT=0xDeployedContractAddressHere
```

4. Start the AnchorChain API so the SDK can talk to it:

```bash
docker compose -f deploy/docker-compose.yml up --build anchorchain-api
```

5. Run the **on-chain** drill:

```bash
python sdk/drills/epls_demo.py --mode=onchain
```

Expected: the drill logs a “resurrection” to AnchorChain and prints the tx hash or receipt.

---

## 5) Kubernetes (local Minikube)

Start Minikube:

```bash
minikube start
kubectl get nodes
```

### 5.1 Apply Kubernetes manifests (quick path)

From repo root:

```bash
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/anchorchain-deployment.yaml
kubectl apply -f deploy/k8s/anchorchain-service.yaml
# optionally:
kubectl apply -f deploy/k8s/prometheus/
kubectl apply -f deploy/k8s/grafana/
```

Get service info:

```bash
kubectl get svc -n immortal-logic
```

If using Minikube, expose locally:

```bash
minikube service anchorchain-api -n immortal-logic
```

### 5.2 Helm (structure provided)

If you prefer Helm charts (recommended for real clusters):

```bash
helm upgrade --install anchorchain deploy/helm/anchorchain \
  --namespace immortal-logic --create-namespace \
  --set image.repository="ghcr.io/nova1000x/anchorchain-api" \
  --set image.tag="latest" \
  --set env.RPC_URL="$RPC_URL" \
  --set env.WALLET_PRIVATE_KEY="$WALLET_PRIVATE_KEY" \
  --set env.CHAIN_ID="$CHAIN_ID"
```

---

## 6) Monitoring (Prometheus + Grafana)

If enabled in Docker/K8s, visit Grafana and import a dashboard JSON (to be added under `deploy/grafana/`).

Typical local URLs:

* Prometheus: `http://localhost:9090`
* Grafana: `http://localhost:3000` (admin/admin by default; change it!)

Look for metrics such as:

* `resurrection_events_total`
* `anchorchain_api_requests_total`
* `ils_verification_pass_total` / `ils_verification_fail_total`

---

## 7) CI/CD (Jenkins pipeline skeleton)

1. Run Jenkins (Docker)

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

2. Create a **Multibranch Pipeline** or classic pipeline with a `Jenkinsfile` like:

```groovy
pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('SDK Tests') {
      steps {
        sh 'python -m venv venv && . venv/bin/activate && pip install -r sdk/requirements.txt && pytest -q'
      }
    }
    stage('Build Images') {
      steps {
        sh 'docker build -f deploy/Dockerfile.anchor -t ghcr.io/nova1000x/anchorchain-api:latest .'
      }
    }
    stage('Push Images') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'ghcr', usernameVariable: 'U', passwordVariable: 'P')]) {
          sh 'echo $P | docker login ghcr.io -u $U --password-stdin'
          sh 'docker push ghcr.io/nova1000x/anchorchain-api:latest'
        }
      }
    }
    stage('Deploy (K8s)') {
      steps {
        sh 'kubectl apply -f deploy/k8s/ -n immortal-logic'
      }
    }
  }
}
```

> Adjust registry, credentials IDs, and steps to your infrastructure.

---

## 8) Running the Resurrection Drill (summary)

**Local (no chain):**

```bash
python sdk/drills/epls_demo.py --mode=local
```

**On-chain (AnchorChain notarization):**

```bash
# ensure AnchorChain API is up and .env is set
python sdk/drills/epls_demo.py --mode=onchain
```

---

## 9) Troubleshooting

* **Docker “address already in use”**: change the port in `.env` and compose file, then rebuild.
* **On-chain errors**: confirm `RPC_URL`, funded `WALLET_PRIVATE_KEY`, correct `CHAIN_ID`, and `ANCHORCHAIN_CONTRACT`.
* **K8s service not reachable**: on Minikube use `minikube service …` to open a tunnel.
* **Windows venv activation blocked**: in PowerShell run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once.

---

## 10) What’s Next (for the DevOps Engineer)

* Wire up real deploy scripts for AnchorChain contracts (Hardhat/Foundry).
* Publish Docker images to GHCR/ACR/ECR and use versioned tags.
* Add Prometheus exporters and Grafana dashboards under `deploy/grafana/`.
* Add automated **resurrection drills** in CI (failover → recover → verify → AnchorChain log).
* Harden secrets via Kubernetes Secrets or an external vault (Akeyless/HashiCorp).

---

**NOVA 1000™ A.C.E.™ Covenant Note**
This deployment guide accompanies sovereign-grade licenses. All production deployments must route continuity events to AnchorChain™ and respect governance enforcement and founder/Trust overrides per the license terms.


