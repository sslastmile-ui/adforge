import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = "gemini-pro"
        
    def generate_creative_dna(self, product_name, offer, target_audience, brand_voice=""):
        prompt = f"""
        You are a D2C marketing expert. Generate a Creative DNA with these exact fields:
        - hook: Attention-grabbing headline (under 10 words)
        - value_prop: Main benefit for the customer
        - cta: Clear call-to-action
        - visual_sentiment: Description for image generation

        Product: {product_name}
        Offer: {offer}
        Target Audience: {target_audience}
        Brand Voice: {brand_voice or "Professional"}

        Return ONLY valid JSON.
        """
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.8, "maxOutputTokens": 1000}
            }
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
            else:
                return self._fallback_dna(product_name, offer)
        except Exception as e:
            return self._fallback_dna(product_name, offer)
    
    def _fallback_dna(self, product_name, offer):
        return {
            "hook": f"Discover the Best {product_name}",
            "value_prop": offer,
            "cta": "Shop Now",
            "visual_sentiment": "Modern, clean, lifestyle photography"
        }