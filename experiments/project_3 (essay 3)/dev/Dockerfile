FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies only needed for compilation
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .

# Remove internal packages not available on PyPI
RUN grep -vE 'flight-exceptions|shared-exceptions|slot-exceptions' requirements.txt > req_fixed.txt && \
    mv req_fixed.txt requirements.txt

# Create virtual environment and install dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Clean up build dependencies
RUN apt-get purge -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

FROM python:3.12-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /venv /venv

# Copy application code (entire project)
COPY --chown=appuser:appuser . .

# Set environment variables
ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run application (fixed port number)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
