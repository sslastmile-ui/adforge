import os 
import logging 
from typing import Dict, List, Optional, Any 
from datetime import datetime 
from collections import defaultdict 
 
logger = logging.getLogger(__name__) 
 
class FallbackManager: 
    def __init__(self, ai_gateway=None): 
        self.ai_gateway = ai_gateway 
        self.fallback_chain = {} 
        self.free_tier_state = defaultdict(lambda: {"used": 0, "limit": 100, "reset_at": None}) 
        self.fallback_history = [] 
        self.paid_allowed = False 
        self._initialize_fallback_chain() 
 
    def _initialize_fallback_chain(self): 
        self.fallback_chain = { 
            "text": ["gemini-pro", "llama-3-70b", "mistral-large", "deepseek-v3", "phi-4"], 
            "image": ["imagen-3", "stable-diffusion-xl", "dall-e-3"], 
            "video": ["veo", "wan", "runway-gen-3-video"], 
            "audio": ["whisper", "elevenlabs", "fish-audio"], 
            "search": ["google-search", "perplexity", "bing-search"] 
        } 
 
    async def get_fallback_provider(self, capability: str, primary_provider: str = None) -
        chain = self.fallback_chain.get(capability, []) 
        if primary_provider and primary_provider in chain: 
            idx = chain.index(primary_provider) 
            chain = chain[idx + 1:] 
        for provider in chain: 
            if self._is_provider_available(provider): 
                return provider 
        return None 
 
    async def get_provider_with_fallback(self, capability: str, free_only: bool = True) -
        if free_only and not self._has_free_quota(capability): 
            logger.warning(f"Free quota exhausted for {capability}, checking fallback") 
            fallback = await self.get_fallback_provider(capability) 
            if fallback: 
                self.fallback_history.append({"capability": capability, "fallback": fallback, "reason": "free_quota_exhausted", "timestamp": datetime.utcnow().isoformat()}) 
                return fallback 
            if self.paid_allowed: 
                logger.info(f"Using paid provider for {capability}") 
                return "openai-gpt-4o" 
            return "none" 
        if self.ai_gateway: 
            route = await self.ai_gateway.route_request(capability, free_only) 
            if route.get("provider"): 
                return route["provider"] 
        chain = self.fallback_chain.get(capability, []) 
        for provider in chain: 
            if self._is_provider_available(provider): 
                return provider 
        return "none" 
 
    def _is_provider_available(self, provider: str) -
        if self.ai_gateway: 
            return self.ai_gateway.registry.check_health(provider) 
        return True 
 
    def _has_free_quota(self, capability: str) -
        state = self.free_tier_state[capability] 
 
    def record_usage(self, capability: str, count: int = 1): 
        self.free_tier_state[capability]["used"] += count 
 
    def reset_free_quota(self, capability: str = None): 
        if capability: 
            self.free_tier_state[capability]["used"] = 0 
            self.free_tier_state[capability]["reset_at"] = datetime.utcnow().isoformat() 
        else: 
            for cap in self.free_tier_state: 
                self.free_tier_state[cap]["used"] = 0 
                self.free_tier_state[cap]["reset_at"] = datetime.utcnow().isoformat() 
 
    def get_statistics(self) -
        return { 
            "free_quota": {cap: {"used": s["used"], "limit": s["limit"], "remaining": s["limit"] - s["used"]} for cap, s in self.free_tier_state.items()}, 
            "fallback_history": len(self.fallback_history), 
            "paid_allowed": self.paid_allowed 
        } 
