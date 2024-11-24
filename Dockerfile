FROM python:3.12-slim

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

# Create volume mount points for input data and results
VOLUME /app/data
VOLUME /app/results

# Create entrypoint script
RUN echo '#!/bin/sh\n\
  if [ -z "$OPENAI_API_KEY" ]; then\n\
  echo "Error: OPENAI_API_KEY environment variable is not set"\n\
  exit 1\n\
  fi\n\
  exec python main.py "$@"' > /app/entrypoint.sh && \
  chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
