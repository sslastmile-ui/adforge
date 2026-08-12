"""Load Balancer - Provider switching based on health, cost, availability.""" 
 
class LoadBalancer: 
    def __init__(self): 
        self.provider_health = {} 
 
    async def select_provider(self, capability, providers): 
        healthy = [] 
        for provider in providers: 
            if self.provider_health.get(provider, {}).get("status") != "unhealthy": 
                healthy.append(provider) 
        return healthy[0] if healthy else None 
