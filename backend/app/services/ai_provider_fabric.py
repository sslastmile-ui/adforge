from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AIProviderFabric:
    def __init__(self):
        self.providers = self._initialize_providers()
        self.active_providers = {}
    
    def _initialize_providers(self) -> Dict:
        return {"gemini": {"category": "text", "models": ["gemini-pro", "gemini-1.5-pro", "gemini-2.0-flash"], "free": True, "api_type": "google"}, "openai": {"category": "text", "models": ["gpt-4o", "gpt-4-turbo", "o3-mini"], "free": False, "api_type": "openai"}, "anthropic": {"category": "text", "models": ["claude-3.5-sonnet", "claude-3-opus"], "free": False, "api_type": "anthropic"}, "meta": {"category": "text", "models": ["llama-3-70b", "llama-3.1-70b", "llama-3.2-90b"], "free": True, "api_type": "meta"}, "mistral": {"category": "text", "models": ["mistral-large", "mistral-small"], "free": True, "api_type": "mistral"}, "deepseek": {"category": "text", "models": ["deepseek-v3", "deepseek-r1"], "free": True, "api_type": "deepseek"}, "stability": {"category": "image", "models": ["stable-diffusion-3.5", "stable-diffusion-xl"], "free": False, "api_type": "stability"}, "openai-image": {"category": "image", "models": ["dall-e-3", "dall-e-2"], "free": False, "api_type": "openai"}, "google-image": {"category": "image", "models": ["imagen-3", "imagen-2"], "free": True, "api_type": "google"}, "runway": {"category": "video", "models": ["gen-3", "gen-2"], "free": False, "api_type": "runway"}, "google-video": {"category": "video", "models": ["veo"], "free": True, "api_type": "google"}, "openai-audio": {"category": "audio", "models": ["whisper"], "free": True, "api_type": "openai"}, "elevenlabs": {"category": "audio", "models": ["elevenlabs", "elevenlabs-pro"], "free": True, "api_type": "elevenlabs"}, "google-search": {"category": "search", "models": ["google-search"], "free": True, "api_type": "google"}, "perplexity": {"category": "search", "models": ["perplexity"], "free": True, "api_type": "perplexity"}}
    
    def get_providers_by_category(self, category: str) -> List[Dict]:
        return [{"name": k, **v} for k, v in self.providers.items() if v["category"] == category]
    
    def get_provider(self, name: str) -> Optional[Dict]:
        return self.providers.get(name)
    
    def get_all_providers(self) -> Dict:
        return self.providers
    
    def get_free_providers(self, category: Optional[str] = None) -> List[Dict]:
        result = []
        for name, provider in self.providers.items():
            if provider["free"] and (category is None or provider["category"] == category):
                result.append({"name": name, **provider})
        return result
    
    def get_paid_providers(self, category: Optional[str] = None) -> List[Dict]:
        result = []
        for name, provider in self.providers.items():
            if not provider["free"] and (category is None or provider["category"] == category):
                result.append({"name": name, **provider})
        return result
    
    def get_statistics(self) -> Dict:
        total = len(self.providers)
        free = len([p for p in self.providers.values() if p["free"]])
        paid = total - free
        categories = {}
        for p in self.providers.values():
            cat = p["category"]
            categories[cat] = categories.get(cat, 0) + 1
        return {"total_providers": total, "free_providers": free, "paid_providers": paid, "categories": categories}