#!/bin/bash

echo "🚀 Starting Immortal Logic AnchorChain Demo..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start the demo stack
echo "📦 Starting Docker services..."
cd /home/ubuntu/test/immortal-logic
docker compose --profile local up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

# Test the API
echo "🧪 Testing API endpoints..."

# Health check
echo "📋 Health check:"
curl -s http://localhost:8000/health | jq '.' || echo "Health check failed"

echo -e "\n📊 Metrics check:"
curl -s http://localhost:8000/metrics | head -5

# Test anchor endpoint
echo -e "\n🔗 Testing anchor endpoint:"
curl -s -X POST http://localhost:8000/anchor \
  -H "Authorization: Bearer demo-token-123" \
  -H "Content-Type: application/json" \
  -d '{"soul_hash": "demo-hash-123", "metadata": "Demo resurrection event"}' | jq '.' || echo "Anchor test failed"

echo -e "\n✅ Demo stack is running!"
echo "🌐 Access URLs:"
echo "  - AnchorChain API: http://localhost:8000"
echo "  - Grafana Dashboard: http://localhost:3000 (admin/admin)"
echo "  - Prometheus: http://localhost:9090"
echo ""
echo "🧪 Run the demo script:"
echo "  python sdk/drills/epls_demo.py --mode=local"
echo ""
echo "🛑 To stop the demo:"
echo "  docker compose down"
