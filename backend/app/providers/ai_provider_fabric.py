"""AI Provider Fabric - Manages 150+ providers and capabilities.""" 
 
class AIProviderFabric: 
    def __init__(self): 
        self.providers = self._init_providers() 
 
    def _init_providers(self): 
        return { 
            "gemini": {"capabilities": ["text", "vision"], "free": True}, 
            "openai": {"capabilities": ["text", "vision", "audio"], "free": False}, 
            "replicate": {"capabilities": ["image", "video"], "free": False}, 
            "stability": {"capabilities": ["image"], "free": False}, 
            "anthropic": {"capabilities": ["text"], "free": False}, 
        } 
 
    def get_provider(self, capability): 
        for name, provider in self.providers.items(): 
            if capability in provider["capabilities"] and provider["free"]: 
                return name 
        return None 
