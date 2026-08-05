import os
import requests
import json
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Use OpenRouter API (or fallback to OpenAI)
        self.api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = os.getenv("AI_MODEL", "meta-llama/llama-4-70b-instruct")
        
    def generate_creative_dna(self, product_name, offer, target_audience, brand_voice=""):
        """Generate Creative DNA using OpenRouter"""
        
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
            response = requests.post(
                url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://adforge.ai",
                    "X-Title": "AdForge"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a D2C marketing expert. Return ONLY valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.8,
                    "response_format": {"type": "json_object"}
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return json.loads(content)
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return self._fallback_dna(product_name, offer)
                
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return self._fallback_dna(product_name, offer)
    
    def _fallback_dna(self, product_name, offer):
        """Fallback DNA if API fails"""
        return {
            "hook": f"Discover the Best {product_name}",
            "value_prop": offer,
            "cta": "Shop Now",
            "visual_sentiment": "Modern, clean, lifestyle photography with warm lighting"
        }