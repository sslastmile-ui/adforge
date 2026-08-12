import os 
import logging 
from typing import Dict, Optional 
from datetime import datetime, timedelta 
from collections import defaultdict 
 
logger = logging.getLogger(__name__) 
 
class CreditManager: 
    def __init__(self, default_quota: int = 100): 
        self.default_quota = default_quota 
        self.quota = defaultdict(lambda: {"used": 0, "limit": default_quota, "reset_at": None}) 
        self.usage_history = [] 
        self.free_credits_remaining = default_quota 
        self.total_free_quota = default_quota 
        self.paid_credits_available = 0 
 
    async def has_credits(self, provider: str = None, amount: int = 1) -
        if provider and provider in self.quota: 
            remaining = self.quota[provider]["limit"] - self.quota[provider]["used"] 
            if remaining 
                return True 
        return self.free_credits_remaining  or self.paid_credits_available 
 
    async def consume(self, provider: str, amount: int = 1) -
        if await self.has_credits(provider, amount): 
            if provider in self.quota: 
                remaining = self.quota[provider]["limit"] - self.quota[provider]["used"] 
                if remaining 
                    self.quota[provider]["used"] += amount 
                    self._log_usage(provider, amount, "quota") 
                    return True 
            if self.free_credits_remaining 
                self.free_credits_remaining -= amount 
                self._log_usage(provider, amount, "free") 
                return True 
            if self.paid_credits_available 
                self.paid_credits_available -= amount 
                self._log_usage(provider, amount, "paid") 
                return True 
        return False 
 
    async def get_remaining(self, provider: str = None) -
        if provider and provider in self.quota: 
            return self.quota[provider]["limit"] - self.quota[provider]["used"] 
        return self.free_credits_remaining + self.paid_credits_available 
 
    async def get_quota(self, provider: str) -
        if provider in self.quota: 
            return {"used": self.quota[provider]["used"], "limit": self.quota[provider]["limit"], "remaining": self.quota[provider]["limit"] - self.quota[provider]["used"]} 
        return {"used": 0, "limit": 0, "remaining": 0} 
 
    async def add_paid_credits(self, amount: int): 
        self.paid_credits_available += amount 
        logger.info(f"Added {amount} paid credits. Total: {self.paid_credits_available}") 
 
    async def reset_free_quota(self): 
        self.free_credits_remaining = self.total_free_quota 
        for provider in self.quota: 
            self.quota[provider]["used"] = 0 
            self.quota[provider]["reset_at"] = datetime.utcnow().isoformat() 
        logger.info("Free quota reset") 
 
    def _log_usage(self, provider: str, amount: int, source: str): 
        self.usage_history.append({"provider": provider, "amount": amount, "source": source, "timestamp": datetime.utcnow().isoformat()}) 
 
    def get_usage_history(self, limit: int = 100) -
        return self.usage_history[-limit:] 
 
    def get_statistics(self) -
        return { 
            "free_remaining": self.free_credits_remaining, 
            "paid_available": self.paid_credits_available, 
            "total_usage": len(self.usage_history), 
            "providers": {p: {"used": d["used"], "limit": d["limit"]} for p, d in self.quota.items()} 
        } 
