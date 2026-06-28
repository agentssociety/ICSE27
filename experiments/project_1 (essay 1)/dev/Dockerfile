FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user to run the application
RUN addgroup --system app && adduser --system --ingroup app appuser

# Set working directory
WORKDIR /app

# Install Python dependencies (production-ready: using --no-cache-dir)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure the non-root user owns the application files
RUN chown -R appuser:app /app

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
