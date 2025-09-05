#!/bin/bash

echo "🚀 AnchorChain Complete Stack Test"
echo "=================================="

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Test 1: Health Check
echo "1. Testing API Health..."
health=$(curl -s http://localhost:8080/health)
echo "   Response: $health"

# Test 2: Anchor Soul States
echo "2. Anchoring Soul States..."
for i in {1..3}; do
    echo "   Anchoring soul state $i..."
    response=$(curl -s -X POST "http://localhost:8080/anchor?soul_hash=0x$(printf '%064d' $i)&metadata=test_$i")
    echo "   Response: $response"
done

# Test 3: Check Metrics
echo "3. Checking Prometheus Metrics..."
metrics=$(curl -s http://localhost:8080/metrics | grep anchorchain_tx)
echo "   Metrics:"
echo "$metrics"

# Test 4: Service Status
echo "4. Service Status Check..."
echo "   AnchorChain API: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)"
echo "   Prometheus: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:9090)"
echo "   Grafana: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)"

echo ""
echo "✅ Stack Test Complete!"
echo ""
echo "🌐 Access Points:"
echo "   • AnchorChain API: http://localhost:8080"
echo "   • Prometheus: http://localhost:9090"
echo "   • Grafana: http://localhost:3000 (admin/admin)"
