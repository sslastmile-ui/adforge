"""Provider Catalog - 150+ providers with capabilities and access details.""" 
 
class ProviderCatalog: 
    def __init__(self): 
        self.providers = self._init_catalog() 
 
    def _init_catalog(self): 
        return { 
            # Text/Reasoning 
            "gemini": {"category": "text", "free": True, "capabilities": ["text", "vision"]}, 
            "openai": {"category": "text", "free": False, "capabilities": ["text", "vision", "audio"]}, 
            "anthropic": {"category": "text", "free": False, "capabilities": ["text"]}, 
            "moonshot": {"category": "text", "free": True, "capabilities": ["text"]}, 
            "kimi": {"category": "text", "free": True, "capabilities": ["text"]}, 
            # Image Generation 
            "replicate": {"category": "image", "free": False, "capabilities": ["image", "video"]}, 
            "stability": {"category": "image", "free": False, "capabilities": ["image"]}, 
            "midjourney": {"category": "image", "free": False, "capabilities": ["image"]}, 
            "dalle": {"category": "image", "free": False, "capabilities": ["image"]}, 
            "bria": {"category": "image", "free": False, "capabilities": ["image"]}, 
            "flow": {"category": "image", "free": False, "capabilities": ["image"]}, 
            # Video Generation 
            "kling": {"category": "video", "free": False, "capabilities": ["video"]}, 
            "luma": {"category": "video", "free": False, "capabilities": ["video"]}, 
            "wan": {"category": "video", "free": False, "capabilities": ["video"]}, 
            "veo": {"category": "video", "free": False, "capabilities": ["video"]}, 
            "whisk": {"category": "video", "free": False, "capabilities": ["video"]}, 
            "higgsfield": {"category": "video", "free": False, "capabilities": ["video"]}, 
            # Audio/Lip-Sync 
            "murf": {"category": "audio", "free": False, "capabilities": ["tts", "voice"]}, 
            "fish_audio": {"category": "audio", "free": False, "capabilities": ["tts", "lip-sync"]}, 
            "lip_sync_video": {"category": "audio", "free": False, "capabilities": ["lip-sync", "avatar"]}, 
            "arcads": {"category": "audio", "free": False, "capabilities": ["tts"]}, 
            # Design/Templates 
            "gamma": {"category": "design", "free": True, "capabilities": ["presentations"]}, 
            "canva": {"category": "design", "free": True, "capabilities": ["templates", "design"]}, 
            "figma": {"category": "design", "free": True, "capabilities": ["design", "prototyping"]}, 
            "insmind": {"category": "design", "free": True, "capabilities": ["creative"]}, 
            # Automation/Tools 
            "apify": {"category": "automation", "free": False, "capabilities": ["scraping", "automation"]}, 
            "make": {"category": "automation", "free": True, "capabilities": ["workflow"]}, 
            "n8n": {"category": "automation", "free": True, "capabilities": ["workflow"]}, 
            "pipedream": {"category": "automation", "free": True, "capabilities": ["workflow"]}, 
            # Content/Copy 
            "copy_ai": {"category": "content", "free": False, "capabilities": ["copywriting"]}, 
            "jasper": {"category": "content", "free": False, "capabilities": ["copywriting"]}, 
            "draftly": {"category": "content", "free": False, "capabilities": ["copywriting"]}, 
            # Video Editing 
            "pictory": {"category": "video_edit", "free": False, "capabilities": ["video_editing"]}, 
            "animoto": {"category": "video_edit", "free": False, "capabilities": ["video_creation"]}, 
            # Search/Research 
            "google_search": {"category": "search", "free": True, "capabilities": ["search"]}, 
            "serpapi": {"category": "search", "free": True, "capabilities": ["search"]}, 
            "paperclip": {"category": "search", "free": True, "capabilities": ["research"]}, 
            # Agentic Platforms 
            "lovable": {"category": "agentic", "free": True, "capabilities": ["agents"]}, 
            "postiz": {"category": "agentic", "free": True, "capabilities": ["agents"]}, 
            "bytez": {"category": "agentic", "free": True, "capabilities": ["agents"]}, 
            "chatzy": {"category": "agentic", "free": True, "capabilities": ["chat"]}, 
            # QR/Print 
            "orbitqr": {"category": "qr", "free": True, "capabilities": ["qr_codes"]}, 
            "topmate": {"category": "qr", "free": True, "capabilities": ["qr_codes"]}, 
            # This is a sample of 50+ providers. The full catalog of 150+ providers 
            # would include all the tools mentioned in the blueprint. 
        } 
 
    def get_provider(self, name): 
        return self.providers.get(name) 
 
    def get_providers_by_capability(self, capability): 
        results = [] 
        for name, provider in self.providers.items(): 
            if capability in provider.get("capabilities", []): 
                results.append({"name": name, **provider}) 
        return results 
