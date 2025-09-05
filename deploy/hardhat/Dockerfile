FROM node:18-alpine

WORKDIR /app

COPY hardhat/package.json .
RUN npm install

COPY hardhat/ .
COPY contracts/ ./contracts/

CMD ["npx", "hardhat", "run", "scripts/deploy.js", "--network", "anvil"]
