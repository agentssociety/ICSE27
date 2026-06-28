FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user and group
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --create-home appuser

# Set the working directory
WORKDIR /app

# Install system dependencies (if needed, e.g., for psycopg2-binary)
# psycopg2-binary ships with its own libpq binaries, so no extra packages are required.
# If you need to compile extensions later, uncomment the next line.
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Remove test/dev dependencies (e.g., pytest) for the production image
RUN sed -i '/^pytest/d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership of the application directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Use exec form for CMD to avoid shell overhead
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
