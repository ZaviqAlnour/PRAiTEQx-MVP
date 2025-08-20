"""
PRAiTEQx MVP - Multi-Model AI System
Main Application Entry Point
"""

import asyncio
import uvicorn
from loguru import logger
from src.api.app import create_app

def main():
    """Main application entry point"""
    logger.info("🚀 Starting PRAiTEQx Multi-Model AI System...")
    logger.info("🧠 Loading 6 Expert Models...")
    
    # Create FastAPI application
    app = create_app()
    
    # Run the application
    logger.info("🌐 Server starting at http://localhost:8000")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()