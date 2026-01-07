#!/usr/bin/env python3
"""
Custom startup script for Hugging Face Spaces
"""

import os
import sys
import time
import logging
from main import app
import uvicorn

def main():
    # Get port from environment, default to 8000
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"Starting server on {host}:{port}", file=sys.stderr)

    # Start the uvicorn server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()