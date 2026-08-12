import os 
import json 
import logging 
import asyncio 
from typing import Dict, List, Optional, Any 
from datetime import datetime 
import uuid 
 
logger = logging.getLogger(__name__) 
 
class ProviderExecutionResult: 
    def __init__(self, provider: str, success: bool, result: Any = None, error: str = None, latency: float = 0, tokens: int = 0, cost: float = 0): 
        self.provider = provider 
        self.success = success 
        self.result = result 
        self.error = error 
        self.latency = latency 
        self.tokens = tokens 
        self.cost = cost 
        self.timestamp = datetime.utcnow().isoformat() 
 
class MultiProviderExecutor: 
    def __init__(self, ai_gateway=None): 
        self.ai_gateway = ai_gateway 
        self.execution_history = [] 
        self.max_parallel = 3 
        self.timeout_seconds = 60 
        self.retry_count = 2 
 
    async def execute_with_failover(self, capability: str, payload: Dict, providers: List[str] = None, free_only: bool = True) -
        if not providers and self.ai_gateway: 
            route = await self.ai_gateway.route_request(capability, free_only) 
            if route.get("provider"): 
                providers = [route["provider"]] 
        if not providers: 
            return ProviderExecutionResult("none", False, error="No providers available") 
 
        for attempt in range(self.retry_count + 1): 
            for provider in providers: 
                result = await self._execute_provider(provider, capability, payload) 
                if result.success: 
                    if self.ai_gateway: 
                        await self.ai_gateway.record_usage(provider, result.tokens, result.cost, True) 
                    self.execution_history.append(result) 
                    return result 
                logger.warning(f"Provider {provider} failed (attempt {attempt + 1}): {result.error}") 
                if self.ai_gateway: 
                    await self.ai_gateway.record_usage(provider, 0, 0, False) 
            logger.info(f"All providers failed, retry {attempt + 1}") 
 
        return ProviderExecutionResult("none", False, error="All providers failed after retries") 
 
    async def execute_parallel(self, capability: str, payloads: List[Dict], providers: List[str] = None, free_only: bool = True) -
        semaphore = asyncio.Semaphore(self.max_parallel) 
        async def execute_one(payload): 
            async with semaphore: 
                return await self.execute_with_failover(capability, payload, providers, free_only) 
        return await asyncio.gather(*[execute_one(p) for p in payloads]) 
 
    async def _execute_provider(self, provider: str, capability: str, payload: Dict) -
        start = datetime.utcnow() 
        try: 
            handler = getattr(self, f"_call_{provider}", None) 
            if handler: 
                result = await handler(payload) 
            else: 
                result = await self._call_generic(provider, capability, payload) 
            latency = (datetime.utcnow() - start).total_seconds() 
            return ProviderExecutionResult(provider, True, result, latency=latency) 
        except Exception as e: 
            latency = (datetime.utcnow() - start).total_seconds() 
            return ProviderExecutionResult(provider, False, error=str(e), latency=latency) 
 
    async def _call_generic(self, provider: str, capability: str, payload: Dict) -
        return {"status": "simulated", "provider": provider, "capability": capability, "payload": payload} 
 
    def get_history(self, limit: int = 100) -
        return [{"provider": r.provider, "success": r.success, "latency": r.latency, "timestamp": r.timestamp} for r in self.execution_history[-limit:]] 
 
    def get_statistics(self) -
        total = len(self.execution_history) 
        if not total: 
            return {"total": 0, "success_rate": 0, "avg_latency": 0} 
        successes = sum(1 for r in self.execution_history if r.success) 
        avg_latency = sum(r.latency for r in self.execution_history) / total 
        return {"total": total, "success_rate": successes / total, "avg_latency": avg_latency} 
