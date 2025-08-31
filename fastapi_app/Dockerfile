FROM python:3.11-slim

WORKDIR /app

# System deps for psycopg2 and audio ops (wave)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create storage dir inside image (bind-mounted anyway)
RUN mkdir -p /storage

EXPOSE 8000
CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-config", "logging.yaml"]
