# Multi-stage build for FastAPI backend
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd -g 1001 python && \
    useradd -m -u 1001 -g python python

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R python:python /app
USER python

# Expose port expected by Hugging Face Spaces
EXPOSE 7860

# Run the application (Hugging Face provides PORT; default to 7860)
CMD ["bash", "-lc", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860}"]
