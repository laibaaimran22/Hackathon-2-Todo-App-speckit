from main import app

# This file is used as the entry point for Hugging Face Spaces
# The app instance is imported from main.py and will be served by the platform

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)