# Use a slim Python 3.12 base image for minimal footprint
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user and group
RUN addgroup --system appgroup && \
    adduser --system --no-create-home --ingroup appgroup appuser

# Set working directory
WORKDIR /app

# Install only production dependencies
# (Note: Dev/test packages like pytest, pytest-asyncio, httpx are excluded)
COPY requirements.txt .
RUN pip install --no-cache-dir \
        fastapi>=0.111.0 \
        uvicorn[standard]>=0.29.0 \
        sqlalchemy>=2.0.0 \
        pydantic>=2.0.0 \
        pydantic-settings>=2.0.0 \
        psycopg2-binary>=2.9.0 \
        alembic>=1.13.0 \
        python-dotenv>=1.0.0 \
    && rm -rf /root/.cache

# Copy the application files
COPY . .

# Change ownership to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Start command for uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
