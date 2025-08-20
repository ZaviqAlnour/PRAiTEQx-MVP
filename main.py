"""
PRAiTEQx MVP - Multi-Model AI System
Updated Main Application Entry Point
"""

import argparse
import sys
from loguru import logger

def main():
    """Enhanced main application entry point"""
    
    parser = argparse.ArgumentParser(description="PRAiTEQx Multi-Expert AI System")
    parser.add_argument("--mode", choices=["api", "ui", "full"], default="full",
                       help="Run mode: api (FastAPI only), ui (Gradio only), or full (both)")
    parser.add_argument("--host", default="0.0.0.0", help="Host address")
    parser.add_argument("--api-port", type=int, default=8000, help="FastAPI port")
    parser.add_argument("--ui-port", type=int, default=7860, help="Gradio port")
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting PRAiTEQx Multi-Expert AI System...")
    logger.info("🧠 6 AI Experts: Chat, Code, Creative, Quick, Logic, Search")
    
    if args.mode == "api":
        from src.api.app import create_app
        import uvicorn
        app = create_app()
        logger.info(f"🌐 FastAPI Server starting at http://{args.host}:{args.api_port}")
        uvicorn.run(app, host=args.host, port=args.api_port, reload=True)
        
    elif args.mode == "ui":
        from src.ui.gradio_interface import create_gradio_app
        logger.info(f"🎨 Gradio UI starting at http://{args.host}:{args.ui_port}")
        interface = create_gradio_app(f"http://{args.host}:{args.api_port}")
        interface.launch(server_name=args.host, server_port=args.ui_port, share=True)
        
    else:  # full mode
        from src.ui.launch import main as launch_main
        launch_main()

if __name__ == "__main__":
    main()