FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY anchorchain_api.py .

# Wait for deployment data
CMD ["sh", "-c", "while [ ! -f /shared/anchor/deployment.json ]; do sleep 1; done && cp /shared/anchor/deployment.json . && uvicorn anchorchain_api:app --host 0.0.0.0 --port 8000"]
