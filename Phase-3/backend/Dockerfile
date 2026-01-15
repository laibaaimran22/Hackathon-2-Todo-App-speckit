FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install uvicorn for production
RUN pip install --no-cache-dir "uvicorn[standard]"

# Copy the rest of the application
COPY . .

# Expose port (Hugging Face Spaces uses PORT environment variable)
EXPOSE 8000

# Create a script to run the application with error handling
RUN echo '#!/bin/bash\nset -e\nif [ -z "$DATABASE_URL" ]; then\n  echo "ERROR: DATABASE_URL environment variable is not set!"\n  exit 1\nfi\nexec python startup.py' > run.sh && chmod +x run.sh

# Run the application
CMD ["./run.sh"]