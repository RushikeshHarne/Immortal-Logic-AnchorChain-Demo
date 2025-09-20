FROM node:18-alpine

WORKDIR /app

# Install foundry
RUN apk add --no-cache curl bash git
RUN curl -L https://foundry.paradigm.xyz | bash || true
RUN mkdir -p /root/.foundry/bin
ENV PATH="/root/.foundry/bin:${PATH}"

# Install foundry manually
RUN wget -O /root/.foundry/bin/foundryup https://raw.githubusercontent.com/foundry-rs/foundry/master/foundryup/foundryup && \
    chmod +x /root/.foundry/bin/foundryup && \
    /root/.foundry/bin/foundryup || true

# Install Python for deployment script
RUN apk add --no-cache python3 py3-pip
RUN pip3 install web3 python-dotenv py-solc-x --break-system-packages
RUN python3 -c "import solcx; solcx.install_solc()"

# Copy contract files
COPY contracts/ ./contracts/
COPY deploy.py ./

# Create shared directory
RUN mkdir -p /shared/anchor

# Simple deployment without foundry for now
CMD ["python3", "deploy.py"]
