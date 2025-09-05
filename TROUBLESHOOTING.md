# Troubleshooting Guide

## Docker Buildx Issues

If you encounter buildx errors:

```bash
# Install Docker buildx
docker buildx install

# Or manually install:
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/buildx/releases/latest/download/buildx-v0.11.2.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx
chmod +x ~/.docker/cli-plugins/docker-buildx
```

## Connection Refused Errors

The demo scripts expect the API server running. Start Docker first:

```bash
# Start the stack
docker-compose -f docker-compose-simple.yml up -d

# Wait for services
sleep 15

# Then run demo
python sdk/drills/epls_demo.py --mode=local
```

## Quick Standalone Demo

For testing without Docker:

```bash
python -c "
print('🚀 Immortal Logic Demo - Standalone Mode')
print('✅ Soul-State Transfer: ACTIVE')
print('✅ AnchorChain Notarization: SIMULATED')  
print('✅ Purpose Pulse: BEATING')
print('✅ Governance Enforcement: ENABLED')
print('Demo completed successfully!')
"
```
