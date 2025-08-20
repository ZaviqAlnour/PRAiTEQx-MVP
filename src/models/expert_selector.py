"""
PRAiTEQx Expert Selector
Intelligently chooses the right expert for each query
"""

import re
from typing import List, Dict, Optional
from loguru import logger
from config.model_config import EXPERT_SELECTION_RULES, MODEL_CONFIGS

class ExpertSelector:
    """Smart expert selection based on query analysis"""
    
    def __init__(self):
        self.rules = EXPERT_SELECTION_RULES
        self.models = MODEL_CONFIGS
        logger.info("🧠 Expert Selector initialized with 6 experts")
    
    def analyze_query(self, query: str) -> Dict[str, float]:
        """Analyze query and return confidence scores for each expert type"""
        query_lower = query.lower()
        scores = {}
        
        # Programming/Code Detection
        code_keywords = ['code', 'python', 'javascript', 'function', 'class', 'algorithm', 
                        'programming', 'debug', 'error', 'syntax', 'api', 'database']
        code_score = sum(1 for kw in code_keywords if kw in query_lower) / len(code_keywords)
        scores['code'] = code_score
        
        # Creative Writing Detection  
        creative_keywords = ['story', 'poem', 'creative', 'write', 'imagine', 'fiction',
                           'character', 'plot', 'narrative', 'essay', 'blog']
        creative_score = sum(1 for kw in creative_keywords if kw in query_lower) / len(creative_keywords)
        scores['creative'] = creative_score
        
        # Search/Research Detection
        search_keywords = ['search', 'find', 'research', 'latest', 'current', 'news',
                         'information', 'data', 'facts', 'recent', 'today']
        search_score = sum(1 for kw in search_keywords if kw in query_lower) / len(search_keywords)
        scores['search'] = search_score
        
        # Logic/Reasoning Detection
        logic_keywords = ['analyze', 'compare', 'explain', 'reasoning', 'logic', 'problem',
                         'solution', 'think', 'calculate', 'math', 'statistics']
        logic_score = sum(1 for kw in logic_keywords if kw in query_lower) / len(logic_keywords)
        scores['reasoning'] = logic_score
        
        # Quick Response Detection (short queries)
        if len(query.split()) <= 5:
            scores['quick'] = 0.8
        else:
            scores['quick'] = 0.2
            
        logger.info(f"📊 Query analysis scores: {scores}")
        return scores
    
    def select_experts(self, query: str, max_experts: int = 2) -> List[str]:
        """Select best experts for the query"""
        scores = self.analyze_query(query)
        
        # Find highest scoring category
        best_category = max(scores.items(), key=lambda x: x[1])
        category, confidence = best_category
        
        # If confidence is low, use default
        if confidence < 0.1:
            category = 'default'
        
        # Get expert list for category
        selected_experts = self.rules.get(category, self.rules['default'])
        
        # Limit number of experts
        selected_experts = selected_experts[:max_experts]
        
        logger.info(f"🎯 Selected experts for '{category}': {selected_experts}")
        return selected_experts
    
    def get_expert_prompt(self, expert_type: str, query: str) -> str:
        """Generate specialized prompt for each expert"""
        prompts = {
            "chat_expert": f"As an intelligent conversation assistant, answer this thoughtfully: {query}",
            "code_expert": f"As a programming expert, provide clean, working code solution: {query}",
            "creative_expert": f"As a creative writing specialist, craft an engaging response: {query}",
            "quick_expert": f"Provide a concise, direct answer: {query}",
            "logic_expert": f"Use logical reasoning and analysis to solve: {query}",
            "search_expert": f"Research and provide factual information about: {query}"
        }
        
        return prompts.get(expert_type, f"Answer this query professionally: {query}")