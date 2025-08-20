"""
PRAiTEQx AI Service
High-level AI service that orchestrates expert selection and response generation
"""

import asyncio
from typing import Dict, List, Optional
from loguru import logger
from .expert_selector import ExpertSelector
from .model_manager import ModelManager

class AIService:
    """Main AI service orchestrating the multi-expert system"""
    
    def __init__(self):
        self.expert_selector = ExpertSelector()
        self.model_manager = ModelManager()
        self.response_cache = {}
        logger.info("🚀 PRAiTEQx AI Service initialized with 6-expert system")
    
    async def process_query(self, query: str, use_multi_expert: bool = True) -> Dict:
        """Process a query through the multi-expert system"""
        logger.info(f"📥 Processing query: {query[:100]}...")
        
        # Check cache first
        cache_key = self._generate_cache_key(query, use_multi_expert)
        if cache_key in self.response_cache:
            logger.info("📦 Returning cached response")
            return self.response_cache[cache_key]
        
        # Select appropriate experts
        selected_experts = self.expert_selector.select_experts(
            query, 
            max_experts=2 if use_multi_expert else 1
        )
        
        # Generate response
        if len(selected_experts) > 1 and use_multi_expert:
            response = await self._multi_expert_response(selected_experts, query)
            response_type = "multi_expert"
        else:
            response = await self._single_expert_response(selected_experts[0], query)
            response_type = "single_expert"
        
        # Prepare result
        result = {
            "query": query,
            "response": response,
            "experts_used": selected_experts,
            "response_type": response_type,
            "timestamp": asyncio.get_event_loop().time(),
            "success": True
        }
        
        # Cache result
        self.response_cache[cache_key] = result
        
        logger.info(f"✅ Query processed successfully using {len(selected_experts)} expert(s)")
        return result
    
    async def _single_expert_response(self, expert_key: str, query: str) -> str:
        """Get response from single expert"""
        specialized_prompt = self.expert_selector.get_expert_prompt(expert_key, query)
        response = await self.model_manager.generate_response(expert_key, specialized_prompt)
        return response
    
    async def _multi_expert_response(self, expert_keys: List[str], query: str) -> str:
        """Get combined response from multiple experts"""
        specialized_prompts = [
            self.expert_selector.get_expert_prompt(expert_key, query) 
            for expert_key in expert_keys
        ]
        
        # Use the first prompt for multi-expert consensus
        response = await self.model_manager.multi_expert_consensus(expert_keys, query)
        return response
    
    def _generate_cache_key(self, query: str, use_multi_expert: bool) -> str:
        """Generate cache key for the query"""
        import hashlib
        content = f"{query}_{use_multi_expert}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    async def get_system_status(self) -> Dict:
        """Get current system status"""
        loaded_models = self.model_manager.get_loaded_models()
        
        return {
            "system": "PRAiTEQx Multi-Expert AI",
            "version": "1.0.0-MVP",
            "loaded_models": loaded_models,
            "available_experts": list(self.expert_selector.models.keys()),
            "cache_size": len(self.response_cache),
            "status": "operational"
        }
    
    async def clear_cache(self):
        """Clear response cache"""
        self.response_cache.clear()
        logger.info("🧹 Response cache cleared")