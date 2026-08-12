import json
from typing import Dict, List, Optional

class HookGenerator:
    HOOK_TYPES = ["curiosity", "problem/solution", "benefit", "contrast", "authority", "proof", "urgency", "local_relevance", "question", "story", "pattern_interrupt", "direct_response"]
    PLATFORM_CONTEXT = {"instagram": {"max_length": 40, "tone": "casual", "emoji": True}, "facebook": {"max_length": 60, "tone": "conversational", "emoji": True}, "linkedin": {"max_length": 80, "tone": "professional", "emoji": False}, "google": {"max_length": 30, "tone": "direct", "emoji": False}, "youtube": {"max_length": 70, "tone": "engaging", "emoji": True}}
    
    def __init__(self):
        self.ai_service = None
    
    async def generate_hooks(self, product_name: str, product_description: str, offer: str, target_audience: str, platform: str = "instagram", hook_types: Optional[List[str]] = None) -> Dict[str, Dict]:
        if hook_types is None:
            hook_types = self.HOOK_TYPES
        context = self.PLATFORM_CONTEXT.get(platform, self.PLATFORM_CONTEXT["instagram"])
        results = {}
        for hook_type in hook_types[:6]:
            results[hook_type] = {"text": f"{hook_type.replace('/', ' ')}: {product_name} - {offer}", "type": hook_type, "score": 0.7 + (len(results) * 0.03)}
        return results
    
    def _score_hook(self, hook: Dict, context: dict) -> float:
        score = 0.0
        text = hook.get("text", "")
        if len(text) <= context["max_length"]:
            score += 0.3
        keywords = ["you", "your", "get", "save", "discover", "unlock"]
        if any(kw in text.lower() for kw in keywords):
            score += 0.3
        urgency_keywords = ["now", "today", "limited", "offer", "discount"]
        if any(kw in text.lower() for kw in urgency_keywords):
            score += 0.2
        emotion_words = ["love", "amazing", "incredible", "best"]
        if any(kw in text.lower() for kw in emotion_words):
            score += 0.2
        return min(score, 1.0)
    
    def _fallback_hook(self, hook_type: str, product: str) -> str:
        fallbacks = {"curiosity": f"Discover the secret behind {product}.", "problem/solution": f"Stop struggling with {product} problems.", "benefit": f"Get the best {product} experience today.", "contrast": f"Better than anything else.", "authority": f"The #1 {product} you need.", "proof": f"Join thousands who love {product}.", "urgency": f"Limited offer ends soon!", "local_relevance": f"Your local {product} experts.", "question": f"Ready for the best {product}?", "story": f"Discover the story behind {product}.", "pattern_interrupt": f"Everything you know about {product} is wrong.", "direct_response": f"Get {product} now!"}
        return fallbacks.get(hook_type, f"Try {product} today!")