#!/bin/bash

echo "Waiting for contract deployment..."

while [ ! -f /shared/anchor/contract.json ]; do
    echo "Contract not deployed yet, waiting..."
    sleep 5
done

echo "Contract found, starting API..."
python -m api.main
