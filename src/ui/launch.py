"""
PRAiTEQx Launch Script
Launches both FastAPI backend and Gradio frontend with environment variables
"""

import asyncio
import threading
import time
import uvicorn
from loguru import logger
from src.api.app import create_app
from src.ui.gradio_interface import create_gradio_app
import os
from dotenv import load_dotenv

def run_fastapi():
    """Run FastAPI backend server"""
    load_dotenv()
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    logger.info(f"🚀 Starting FastAPI backend at http://{host}:{port}...")
    app = create_app()
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,  # Disable reload in production
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )

def run_gradio():
    """Run Gradio frontend"""
    load_dotenv()
    host = os.getenv("API_HOST", "0.0.0.0")
    api_port = int(os.getenv("API_PORT", 8000))
    ui_port = int(os.getenv("UI_PORT", 7860))
    
    logger.info(f"🎨 Starting Gradio frontend at http://{host}:{ui_port}...")
    time.sleep(3)  # Wait for FastAPI to start
    
    interface = create_gradio_app(f"http://{host}:{api_port}")
    interface.launch(
        server_name=host,
        server_port=ui_port,
        share=True,  # This creates a public URL
        show_error=True
    )

def main():
    """Main launcher function"""
    logger.info("🚀 Launching PRAiTEQx Multi-Expert AI System...")
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Start Gradio in main thread
    run_gradio()

if __name__ == "__main__":
    main()