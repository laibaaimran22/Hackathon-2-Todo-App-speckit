#!/usr/bin/env python3
"""
Custom startup script for Hugging Face Spaces
"""

import os
import sys
import time
import logging
import threading
import asyncio
from main import app
import uvicorn

# Import event handlers
from event_handlers import run_scheduler

def run_scheduler_thread():
    """Run the scheduler in a separate thread"""
    asyncio.run(run_scheduler())

def main():
    # Get port from environment, default to 8000
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"Starting Todo Chatbot Backend on {host}:{port}", file=sys.stderr)
    print(f"API endpoints available at /", file=sys.stderr)
    print(f"MCP endpoints available at /mcp/", file=sys.stderr)

    # Start the scheduler in a background thread
    scheduler_thread = threading.Thread(target=run_scheduler_thread, daemon=True)
    scheduler_thread.start()

    # Start the uvicorn server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()