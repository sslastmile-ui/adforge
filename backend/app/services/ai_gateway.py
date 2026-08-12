import os
import json
import logging
import random
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

class AIProviderRegistry:
    def __init__(self):
        self.providers = self._build_registry()
        self.provider_health = defaultdict(lambda: {"healthy": True, "last_check": None, "failures": 0})
        self.quota_tracker = defaultdict(lambda: {"used": 0, "limit": 0, "reset_at": None})
    
    def _build_registry(self) -> Dict:
        return {
            "gemini-pro": {"capability": "text", "free": True, "quota": 100, "cost": 0},
            "gemini-1.5-pro": {"capability": "text", "free": True, "quota": 50, "cost": 0},
            "openai-gpt-4o": {"capability": "text", "free": False, "quota": 0, "cost": 0.005},
            "claude-3.5-sonnet": {"capability": "text", "free": False, "quota": 0, "cost": 0.003},
            "llama-3-70b": {"capability": "text", "free": True, "quota": 100, "cost": 0},
            "mistral-large": {"capability": "text", "free": True, "quota": 50, "cost": 0},
            "deepseek-v3": {"capability": "text", "free": True, "quota": 100, "cost": 0},
            "phi-4": {"capability": "text", "free": True, "quota": 100, "cost": 0},
            "gemma-2": {"capability": "text", "free": True, "quota": 100, "cost": 0},
            "stable-diffusion-3.5": {"capability": "image", "free": False, "quota": 0, "cost": 0.002},
            "stable-diffusion-xl": {"capability": "image", "free": False, "quota": 0, "cost": 0.001},
            "dall-e-3": {"capability": "image", "free": False, "quota": 0, "cost": 0.04},
            "imagen-3": {"capability": "image", "free": True, "quota": 10, "cost": 0},
            "veo": {"capability": "video", "free": True, "quota": 5, "cost": 0},
            "whisper": {"capability": "audio", "free": True, "quota": 100, "cost": 0},
            "elevenlabs": {"capability": "audio", "free": True, "quota": 20, "cost": 0}
        }
    
    def get_providers_for_capability(self, capability: str, free_only: bool = True) -> List[Dict]:
        results = []
        for name, provider in self.providers.items():
            if provider["capability"] == capability and (not free_only or provider["free"]):
                results.append({"name": name, **provider})
        return results
    
    def check_health(self, provider: str) -> bool:
        health = self.provider_health[provider]
        if not health["healthy"] and health.get("last_check"):
            cooldown = datetime.fromisoformat(health["last_check"])
            if datetime.utcnow() - cooldown > timedelta(minutes=5):
                health["healthy"] = True
        return health["healthy"]
    
    def mark_unhealthy(self, provider: str):
        self.provider_health[provider]["healthy"] = False
        self.provider_health[provider]["last_check"] = datetime.utcnow().isoformat()
        self.provider_health[provider]["failures"] += 1
    
    def get_quota(self, provider: str) -> Dict:
        return self.quota_tracker[provider]

class AIGateway:
    def __init__(self):
        self.registry = AIProviderRegistry()
        self.circuit_breakers = defaultdict(lambda: {"open": False, "last_failure": None})
    
    async def route_request(self, capability: str, free_only: bool = True, tenant_id: Optional[str] = None) -> Dict:
        providers = self.registry.get_providers_for_capability(capability, free_only)
        if not providers:
            return {"error": f"No {capability} providers available", "fallback_used": True}
        providers.sort(key=lambda x: x["cost"])
        for provider in providers:
            if self.circuit_breakers[provider["name"]]["open"]:
                continue
            quota = self.registry.get_quota(provider["name"])
            if quota["used"] >= quota["limit"] and quota["limit"] > 0:
                continue
            if not self.registry.check_health(provider["name"]):
                continue
            return {"provider": provider["name"], "capability": capability, "free": provider["free"], "cost": provider["cost"], "quota_remaining": quota["limit"] - quota["used"] if quota["limit"] > 0 else "unlimited"}
        return {"error": f"No healthy {capability} providers with available quota", "fallback_used": True}
    
    async def record_usage(self, provider: str, tokens: int = 0, cost: float = 0.0, success: bool = True):
        if success:
            self.registry.quota_tracker[provider]["used"] += 1
        else:
            self.registry.mark_unhealthy(provider)
            self.circuit_breakers[provider]["last_failure"] = datetime.utcnow().isoformat()
            if self.registry.provider_health[provider]["failures"] >= 3:
                self.circuit_breakers[provider]["open"] = True
    
    def get_all_providers(self) -> Dict:
        return self.registry.providers
    
    def get_provider_stats(self, provider: str) -> Dict:
        return {"name": provider, "health": self.registry.check_health(provider), "quota": self.registry.get_quota(provider), "circuit_breaker": self.circuit_breakers[provider]}