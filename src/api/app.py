"""
PRAiTEQx FastAPI Application
Main API backend for the Multi-Expert AI System
"""

import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger
import time

from src.models.ai_service import AIService

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    use_multi_expert: Optional[bool] = True
    max_experts: Optional[int] = 2

class QueryResponse(BaseModel):
    success: bool
    query: str
    response: str
    experts_used: list
    response_type: str
    processing_time: float
    timestamp: float

class SystemStatus(BaseModel):
    system: str
    version: str
    loaded_models: list
    available_experts: list
    cache_size: int
    status: str

# Initialize AI Service
ai_service = None

async def get_ai_service():
    """Get or initialize AI service"""
    global ai_service
    if ai_service is None:
        ai_service = AIService()
        logger.info("🚀 AI Service initialized")
    return ai_service

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="PRAiTEQx Multi-Expert AI System",
        description="Advanced AI system with 6 specialized experts working in harmony",
        version="1.0.0-MVP",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this properly in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        logger.info("🚀 Starting PRAiTEQx API Server...")
        await get_ai_service()
        logger.info("✅ Server ready to handle requests!")
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "🧠 PRAiTEQx Multi-Expert AI System",
            "version": "1.0.0-MVP",
            "docs": "/docs",
            "status": "operational"
        }
    
    @app.post("/query", response_model=QueryResponse)
    async def process_query(request: QueryRequest):
        """Process AI query through multi-expert system"""
        try:
            start_time = time.time()
            service = await get_ai_service()
            
            logger.info(f"📥 New query received: {request.query[:100]}...")
            
            # Process query through AI service
            result = await service.process_query(
                query=request.query,
                use_multi_expert=request.use_multi_expert
            )
            
            processing_time = time.time() - start_time
            
            return QueryResponse(
                success=result["success"],
                query=result["query"],
                response=result["response"],
                experts_used=result["experts_used"],
                response_type=result["response_type"],
                processing_time=processing_time,
                timestamp=result["timestamp"]
            )
            
        except Exception as e:
            logger.error(f"❌ Error processing query: {e}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    @app.get("/status", response_model=SystemStatus)
    async def get_system_status():
        """Get current system status"""
        try:
            service = await get_ai_service()
            status = await service.get_system_status()
            
            return SystemStatus(**status)
            
        except Exception as e:
            logger.error(f"❌ Error getting system status: {e}")
            raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")
    
    @app.post("/clear-cache")
    async def clear_cache():
        """Clear response cache"""
        try:
            service = await get_ai_service()
            await service.clear_cache()
            return {"message": "✅ Cache cleared successfully"}
            
        except Exception as e:
            logger.error(f"❌ Error clearing cache: {e}")
            raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")
    
    @app.get("/experts")
    async def get_available_experts():
        """Get list of available AI experts"""
        from config.model_config import MODEL_CONFIGS
        
        experts = {}
        for key, config in MODEL_CONFIGS.items():
            experts[key] = {
                "name": config.name,
                "expert_type": config.expert_type,
                "max_tokens": config.max_tokens,
                "temperature": config.temperature
            }
        
        return {
            "total_experts": len(experts),
            "experts": experts
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "system": "PRAiTEQx Multi-Expert AI"
        }
    
    return app