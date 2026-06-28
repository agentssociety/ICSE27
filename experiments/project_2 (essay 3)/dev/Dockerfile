# Use official Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables to avoid Python buffering and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Create a non-root user with a specific UID/GID
RUN addgroup --gid 1001 appgroup && \
    adduser --uid 1001 --gid 1001 --disabled-password --gecos "" appuser

# Install system dependencies only if needed (psycopg2-binary may need libpq)
# For psycopg2-binary, the binary wheel includes the library, so no extra packages.
# If you encounter issues, uncomment next line:
# RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Switch to non-root user for security
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
