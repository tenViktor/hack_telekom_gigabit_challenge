FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
  wget \
  gnupg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps

# Copy the rest of the application
COPY . .

# Create volume mount point for results
VOLUME /app/results

ENTRYPOINT ["python", "main.py"]
