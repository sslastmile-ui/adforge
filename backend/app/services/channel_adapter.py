from typing import Dict, List, Any
import json

class ChannelAdapter:
    CHANNELS = ["instagram", "facebook", "google", "linkedin", "pinterest", "whatsapp", "youtube"]
    
    def __init__(self):
        self.channel_configs = {"instagram": {"max_caption": 2200, "max_hashtags": 30, "image_count": 10}, "facebook": {"max_text": 63206, "image_count": 10}, "google": {"headlines": 3, "descriptions": 2, "display_paths": 2}, "linkedin": {"max_content": 3000, "image_count": 9}, "pinterest": {"max_title": 100, "max_description": 500}, "whatsapp": {"max_message": 4096}, "youtube": {"max_title": 100, "max_description": 5000}}
    
    async def adapt(self, channel: str, content: Dict) -> Dict:
        if channel not in self.CHANNELS:
            return {"error": f"Channel {channel} not supported"}
        adapter_method = getattr(self, f"_adapt_{channel}", None)
        if adapter_method:
            return await adapter_method(content)
        return self._generic_adapt(channel, content)
    
    async def _adapt_instagram(self, content: Dict) -> Dict:
        return {"caption": content.get("caption", ""), "hashtags": content.get("hashtags", ""), "image_prompt": content.get("image_prompt", ""), "first_comment": content.get("first_comment", ""), "carousel": content.get("carousel", [])}
    
    async def _adapt_facebook(self, content: Dict) -> Dict:
        return {"primary_text": content.get("primary_text", ""), "headline": content.get("headline", ""), "description": content.get("description", ""), "call_to_action": content.get("call_to_action", ""), "image_url": content.get("image_url", "")}
    
    async def _adapt_google(self, content: Dict) -> Dict:
        return {"headlines": content.get("headlines", []), "descriptions": content.get("descriptions", []), "display_paths": content.get("display_paths", ["shop", "sale"]), "final_url": content.get("final_url", "https://example.com"), "call_to_action": content.get("call_to_action", "Shop Now")}
    
    async def _adapt_linkedin(self, content: Dict) -> Dict:
        return {"title": content.get("title", ""), "content": content.get("content", ""), "company_mention": content.get("company_mention", ""), "cta": content.get("cta", ""), "image_prompt": content.get("image_prompt", "")}
    
    async def _adapt_pinterest(self, content: Dict) -> Dict:
        return {"title": content.get("title", ""), "description": content.get("description", ""), "board_id": content.get("board_id", ""), "image_prompt": content.get("image_prompt", ""), "link": content.get("link", "")}
    
    async def _adapt_whatsapp(self, content: Dict) -> Dict:
        return {"message": content.get("message", ""), "template": content.get("template", ""), "media_url": content.get("media_url", "")}
    
    async def _adapt_youtube(self, content: Dict) -> Dict:
        return {"title": content.get("title", ""), "description": content.get("description", ""), "tags": content.get("tags", []), "thumbnail_prompt": content.get("thumbnail_prompt", "")}
    
    def _generic_adapt(self, channel: str, content: Dict) -> Dict:
        return {"channel": channel, "content": content}
    
    def get_channel_config(self, channel: str) -> Dict:
        return self.channel_configs.get(channel, {})
    
    def list_channels(self) -> List[str]:
        return self.CHANNELS