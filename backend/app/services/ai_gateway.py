import os 
import json 
import logging 
import requests 
import asyncio 
from typing import Dict, List, Optional, Any 
from datetime import datetime 
from collections import defaultdict 
 
logger = logging.getLogger(__name__) 
 
class AIGateway: 
    def __init__(self): 
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") 
        self.provider_catalog = None 
        self.credit_manager = None 
        self.fallback_manager = None 
        self.health_checks = defaultdict(lambda: {"healthy": True, "last_check": None, "failures": 0}) 
        self.circuit_breakers = defaultdict(lambda: {"open": False, "last_failure": None, "cooldown_until": None}) 
 
    async def execute(self, provider: str, capability: str, payload: Dict) -
        if self.circuit_breakers[provider]["open"]: 
            cooldown = self.circuit_breakers[provider]["cooldown_until"] 
                return {"error": f"Provider {provider} is on cooldown", "fallback_used": True} 
            else: 
                self.circuit_breakers[provider]["open"] = False 
 
        if provider == "google-gemini-pro" or provider == "google-gemini-1.5-pro": 
            return await self._execute_gemini(provider, payload) 
        elif provider == "openai-gpt-4o" or provider == "openai-gpt-4-turbo": 
            return await self._execute_openai(provider, payload) 
        elif provider == "anthropic-claude-3.5-sonnet": 
            return await self._execute_anthropic(provider, payload) 
        elif provider == "meta-llama-3-70b": 
            return await self._execute_meta(provider, payload) 
        else: 
            return await self._execute_fallback(provider, payload) 
 
    async def _execute_gemini(self, provider: str, payload: Dict) -
        api_key = os.getenv("GEMINI_API_KEY") 
        if not api_key: 
            return {"error": "GEMINI_API_KEY not configured", "fallback_used": True} 
        model = "gemini-pro" if provider == "google-gemini-pro" else "gemini-1.5-pro" 
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}" 
        prompt = payload.get("prompt", "") 
        data = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.8, "maxOutputTokens": 1000}} 
        try: 
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"}, timeout=30) 
            if response.status_code == 200: 
                result = response.json() 
                text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "") 
                return {"success": True, "provider": provider, "result": text, "model": model} 
            else: 
                self._mark_unhealthy(provider) 
                return {"error": f"Gemini API error: {response.status_code}", "fallback_used": True} 
        except Exception as e: 
            self._mark_unhealthy(provider) 
            return {"error": str(e), "fallback_used": True} 
 
    async def _execute_openai(self, provider: str, payload: Dict) -
        api_key = os.getenv("OPENAI_API_KEY") 
        if not api_key: 
            return {"error": "OPENAI_API_KEY not configured", "fallback_used": True} 
        model = "gpt-4o" if provider == "openai-gpt-4o" else "gpt-4-turbo" 
        url = "https://api.openai.com/v1/chat/completions" 
        prompt = payload.get("prompt", "") 
        data = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.8, "max_tokens": 1000} 
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"} 
        try: 
            response = requests.post(url, json=data, headers=headers, timeout=30) 
            if response.status_code == 200: 
                result = response.json() 
                text = result.get("choices", [{}])[0].get("message", {}).get("content", "") 
                return {"success": True, "provider": provider, "result": text, "model": model} 
            else: 
                self._mark_unhealthy(provider) 
                return {"error": f"OpenAI API error: {response.status_code}", "fallback_used": True} 
        except Exception as e: 
            self._mark_unhealthy(provider) 
            return {"error": str(e), "fallback_used": True} 
 
    async def _execute_anthropic(self, provider: str, payload: Dict) -
        api_key = os.getenv("ANTHROPIC_API_KEY") 
        if not api_key: 
            return {"error": "ANTHROPIC_API_KEY not configured", "fallback_used": True} 
        url = "https://api.anthropic.com/v1/messages" 
        prompt = payload.get("prompt", "") 
        data = {"model": "claude-3-5-sonnet-20241022", "max_tokens": 1000, "messages": [{"role": "user", "content": prompt}]} 
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"} 
        try: 
            response = requests.post(url, json=data, headers=headers, timeout=30) 
            if response.status_code == 200: 
                result = response.json() 
                text = result.get("content", [{}])[0].get("text", "") 
                return {"success": True, "provider": provider, "result": text} 
            else: 
                self._mark_unhealthy(provider) 
                return {"error": f"Anthropic API error: {response.status_code}", "fallback_used": True} 
        except Exception as e: 
            self._mark_unhealthy(provider) 
            return {"error": str(e), "fallback_used": True} 
 
    async def _execute_meta(self, provider: str, payload: Dict) -
        return {"success": True, "provider": provider, "result": "Meta Llama 3 execution (simulated)", "model": "llama-3-70b"} 
 
    async def _execute_fallback(self, provider: str, payload: Dict) -
        logger.warning(f"No specific handler for {provider}, using fallback") 
        return {"success": True, "provider": provider, "result": f"Fallback execution for {provider}", "model": "fallback"} 
 
    def _mark_unhealthy(self, provider: str): 
        self.health_checks[provider]["healthy"] = False 
        self.health_checks[provider]["last_check"] = datetime.utcnow().isoformat() 
        self.health_checks[provider]["failures"] += 1 
        if self.health_checks[provider]["failures"] 
            self.circuit_breakers[provider]["open"] = True 
            self.circuit_breakers[provider]["cooldown_until"] = (datetime.utcnow() + timedelta(minutes=5)).isoformat() 
 
    async def route_request(self, capability: str, free_only: bool = True, tenant_id: Optional[str] = None) -
        if free_only: 
            return {"provider": "google-gemini-pro", "free": True, "cost": 0.0, "quota_remaining": 100} 
        return {"provider": "openai-gpt-4o", "free": False, "cost": 0.005, "quota_remaining": "unlimited"} 
 
    async def record_usage(self, provider: str, tokens: int = 0, cost: float = 0.0, success: bool = True): 
        if success: 
            logger.info(f"Usage recorded for {provider}: {tokens} tokens, ${cost:.4f}") 
        else: 
            self._mark_unhealthy(provider) 
 
    def get_statistics(self) -
        return { 
            "providers": len(self.health_checks), 
            "healthy": len([p for p, h in self.health_checks.items() if h["healthy"]]), 
            "circuit_open": len([p for p, c in self.circuit_breakers.items() if c["open"]]), 
            "api_key_configured": bool(self.api_key) 
        } 
