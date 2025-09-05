#!/bin/bash

echo "🚀 AnchorChain Demo Stack Test Suite"
echo "===================================="

# Test 1: Health Check
echo "1. Testing API Health..."
health=$(curl -s http://localhost:8080/health)
echo "   Response: $health"

# Test 2: Anchor Soul States
echo "2. Anchoring Soul States..."
echo "   Anchoring soul state 1..."
anchor1=$(curl -s -X POST "http://localhost:8080/anchor?soul_hash=0x1111111111111111&metadata=resurrection_test_1")
echo "   Response: $anchor1"

echo "   Anchoring soul state 2..."
anchor2=$(curl -s -X POST "http://localhost:8080/anchor?soul_hash=0x2222222222222222&metadata=immortal_logic_demo")
echo "   Response: $anchor2"

echo "   Anchoring soul state 3..."
anchor3=$(curl -s -X POST "http://localhost:8080/anchor?soul_hash=0x3333333333333333&metadata=nova_1000_ace")
echo "   Response: $anchor3"

# Test 3: Retrieve Soul States
echo "3. Retrieving Soul States..."
states=$(curl -s "http://localhost:8080/soul-state/0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
echo "   Response: $states"

# Test 4: Check Metrics
echo "4. Checking Prometheus Metrics..."
metrics=$(curl -s http://localhost:8080/metrics | grep anchorchain_tx)
echo "   Metrics:"
echo "$metrics"

# Test 5: Prometheus Query
echo "5. Testing Prometheus Integration..."
prom_query=$(curl -s "http://localhost:9090/api/v1/query?query=anchorchain_tx_ok_total")
echo "   Prometheus Query Result: $prom_query"

# Test 6: Service Status
echo "6. Service Status Check..."
echo "   AnchorChain API: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)"
echo "   Prometheus: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:9090)"
echo "   Grafana: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)"

echo ""
echo "✅ Demo Stack Test Complete!"
echo ""
echo "🌐 Access Points:"
echo "   • AnchorChain API: http://localhost:8080"
echo "   • Prometheus: http://localhost:9090"
echo "   • Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "📊 Key Metrics Available:"
echo "   • anchorchain_tx_ok_total - Successful transactions"
echo "   • anchorchain_tx_err_total - Failed transactions"
