import os
import json
import logging
from google import genai

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = "gemini-3.6-flash"

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=self.api_key)

    def generate_creative_dna(
        self,
        product_name,
        offer,
        target_audience,
        brand_voice=""
    ):
        """
        Generate Creative DNA using Gemini SDK
        """

        prompt = f"""
You are an expert D2C Marketing Strategist.

Generate ONLY valid JSON.

Required JSON format:

{{
    "hook":"",
    "value_prop":"",
    "cta":"",
    "visual_sentiment":""
}}

Product:
{product_name}

Offer:
{offer}

Target Audience:
{target_audience}

Brand Voice:
{brand_voice or "Professional"}

Do not return markdown.
Do not return explanation.
Return JSON only.
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = response.text.strip()

            # Remove markdown if Gemini adds it
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

            return json.loads(text)

        except Exception as e:

            logger.error(f"Gemini Error: {e}")

            return self._fallback_dna(product_name, offer)

    def _fallback_dna(self, product_name, offer):

        return {
            "hook": f"Discover the Best {product_name}",
            "value_prop": offer,
            "cta": "Shop Now",
            "visual_sentiment": "Modern clean lifestyle photography"
        }