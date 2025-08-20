"""
PRAiTEQx Model Configuration
6-Expert AI System Configuration
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ModelConfig:
    """Individual model configuration"""
    name: str
    model_id: str
    expert_type: str
    load_in_4bit: bool = True
    max_tokens: int = 2048
    temperature: float = 0.7
    
# Our 6-Expert AI Army Configuration
MODEL_CONFIGS = {
    "chat_expert": ModelConfig(
        name="Qwen2.5 Chat Expert",
        model_id="Qwen/Qwen2.5-7B-Instruct", 
        expert_type="chat_reasoning",
        max_tokens=4096,
        temperature=0.7
    ),
    
    "code_expert": ModelConfig(
        name="CodeLlama Programming Expert", 
        model_id="codellama/CodeLlama-7b-Instruct-hf",
        expert_type="programming",
        max_tokens=8192,
        temperature=0.1
    ),
    
    "creative_expert": ModelConfig(
        name="Mistral Creative Expert",
        model_id="mistralai/Mistral-7B-Instruct-v0.2",
        expert_type="creative_writing", 
        max_tokens=4096,
        temperature=0.9
    ),
    
    "quick_expert": ModelConfig(
        name="Gemma Quick Response Expert",
        model_id="google/gemma-7b-it",
        expert_type="quick_response",
        max_tokens=1024, 
        temperature=0.5
    ),
    
    "logic_expert": ModelConfig(
        name="Phi-3 Logic Expert",
        model_id="microsoft/Phi-3-mini-4k-instruct", 
        expert_type="logical_reasoning",
        max_tokens=4096,
        temperature=0.3
    ),
    
    "search_expert": ModelConfig(
        name="BGE Web Search Expert",
        model_id="BAAI/bge-m3",
        expert_type="web_retrieval",
        max_tokens=512,
        temperature=0.1
    )
}

# Expert Selection Rules
EXPERT_SELECTION_RULES = {
    "code": ["code_expert", "logic_expert"],
    "programming": ["code_expert", "logic_expert"], 
    "creative": ["creative_expert", "chat_expert"],
    "writing": ["creative_expert", "chat_expert"],
    "quick": ["quick_expert"],
    "search": ["search_expert", "chat_expert"],
    "reasoning": ["logic_expert", "chat_expert"],
    "default": ["chat_expert"]
}

# System Settings
SYSTEM_CONFIG = {
    "max_concurrent_models": 3,
    "response_timeout": 30,
    "enable_caching": True,
    "cache_size": 1000,
    "log_level": "INFO"
}