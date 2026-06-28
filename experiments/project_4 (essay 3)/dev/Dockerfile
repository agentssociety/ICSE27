FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies required by psycopg2 (or any other native packages)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user early (used later for runtime)
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install only production dependencies (exclude test/development packages)
RUN grep -vE "^(pytest|httpx)" requirements.txt > requirements-prod.txt && \
    pip install --no-cache-dir -r requirements-prod.txt && \
    rm requirements-prod.txt requirements.txt

# Copy application code and set ownership
COPY . .
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
