FROM python:3.12-slim

# Environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non‑root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --uid 1000 appuser

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies (pre‑compiled wheels, no build tools needed)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Switch to the non‑root user
USER appuser

# Expose port 8000 for the uvicorn server
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
