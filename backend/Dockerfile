FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  git \
  sqlmap \
  default-jre \  
  wget \
  && rm -rf /var/lib/apt/lists/*

# Install ZAP
RUN wget https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2.14.0_Linux.tar.gz \
  && tar -xf ZAP_2.14.0_Linux.tar.gz \
  && rm ZAP_2.14.0_Linux.tar.gz
# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /data/sqlmap_results /data/screenshots

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
