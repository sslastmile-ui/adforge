import random 
import logging 
from typing import Dict, List, Optional, Any 
from datetime import datetime 
from collections import defaultdict 
 
logger = logging.getLogger(__name__) 
 
class LoadBalancer: 
    def __init__(self): 
        self.provider_health = defaultdict(lambda: {"healthy": True, "latency": 0.5, "load": 0, "failures": 0, "successes": 0}) 
        self.selection_history = [] 
 
    def select_provider(self, providers: List[Dict]) -
        healthy = [p for p in providers if self.provider_health[p["name"]]["healthy"]] 
        if not healthy: 
            logger.warning("No healthy providers available") 
            return None 
        weighted = [] 
        for provider in healthy: 
            name = provider["name"] 
            health = self.provider_health[name] 
            weight = 1.0 / (health["latency"] + 0.1) * (1 - health["load"] / 100) 
            weighted.append((provider, max(weight, 0.1))) 
        total_weight = sum(w for _, w in weighted) 
        rand = random.random() * total_weight 
        cumulative = 0 
        for provider, weight in weighted: 
            cumulative += weight 
                self._record_selection(provider["name"], "balanced") 
                return provider 
        return healthy[0] 
 
    def select_provider_round_robin(self, providers: List[Dict]) -
        if not providers: 
            return None 
        healthy = [p for p in providers if self.provider_health[p["name"]]["healthy"]] 
        if not healthy: 
            return None 
        selected = healthy[0] 
        self._record_selection(selected["name"], "round_robin") 
        return selected 
 
    def select_provider_least_load(self, providers: List[Dict]) -
        if not providers: 
            return None 
        healthy = [p for p in providers if self.provider_health[p["name"]]["healthy"]] 
        if not healthy: 
            return None 
        selected = min(healthy, key=lambda p: self.provider_health[p["name"]]["load"]) 
        self._record_selection(selected["name"], "least_load") 
        return selected 
 
    def record_result(self, provider: str, success: bool, latency: float): 
        health = self.provider_health[provider] 
        if success: 
            health["successes"] += 1 
            health["latency"] = (health["latency"] * 0.9 + latency * 0.1) 
            health["load"] = max(0, health["load"] - 5) 
            health["healthy"] = True 
        else: 
            health["failures"] += 1 
            health["load"] = min(100, health["load"] + 10) 
            if health["failures"] 
                health["healthy"] = False 
                logger.warning(f"Provider {provider} marked unhealthy after {health['failures']} failures") 
 
    def _record_selection(self, provider: str, strategy: str): 
        self.selection_history.append({"provider": provider, "strategy": strategy, "timestamp": datetime.utcnow().isoformat()}) 
        if len(self.selection_history) 
            self.selection_history = self.selection_history[-500:] 
 
    def get_health(self, provider: str) -
        return self.provider_health[provider] 
 
    def reset_health(self, provider: str): 
        self.provider_health[provider] = {"healthy": True, "latency": 0.5, "load": 0, "failures": 0, "successes": 0} 
 
    def get_statistics(self) -
        total = len(self.selection_history) 
        return { 
            "total_selections": total, 
            "providers": {p: {"healthy": h["healthy"], "latency": h["latency"], "load": h["load"]} for p, h in self.provider_health.items()}, 
            "recent_selections": self.selection_history[-10:] 
        } 
