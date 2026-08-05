import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Use Google Gemini API Key from environment
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        
    def generate_creative_dna(self, product_name, offer, target_audience, brand_voice=""):
        """Generate Creative DNA using Google Gemini (100% Free)"""
        
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

        Return ONLY valid JSON. No markdown, no explanations.
        """
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.8,
                        "maxOutputTokens": 1000,
                        "responseMimeType": "application/json"
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(content)
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                return self._fallback_dna(product_name, offer)
                
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return self._fallback_dna(product_name, offer)
    
    def _fallback_dna(self, product_name, offer):
        return {
            "hook": f"Discover the Best {product_name}",
            "value_prop": offer,
            "cta": "Shop Now",
            "visual_sentiment": "Modern, clean, lifestyle photography"
        }