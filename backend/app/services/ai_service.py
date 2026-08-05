import os
import json
import logging
import requests

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        # Read API key from environment
        self.api_key = os.getenv("GEMINI_API_KEY")

        # Current Gemini model
        self.model = "gemini-2.5-flash"

    def generate_creative_dna(
        self,
        product_name,
        offer,
        target_audience,
        brand_voice=""
    ):
        """Generate Creative DNA using Google Gemini"""

        if not self.api_key:
            logger.error("GEMINI_API_KEY is missing.")
            return self._fallback_dna(product_name, offer)

        prompt = f"""
You are an expert D2C marketing strategist.

Generate ONLY valid JSON.

Required JSON format:

{{
  "hook": "...",
  "value_prop": "...",
  "cta": "...",
  "visual_sentiment": "..."
}}

Requirements:
- hook: under 10 words
- value_prop: concise benefit
- cta: strong call-to-action
- visual_sentiment: image generation description

Product: {product_name}
Offer: {offer}
Target Audience: {target_audience}
Brand Voice: {brand_voice or "Professional"}

Return ONLY JSON.
"""

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.model}:generateContent?key={self.api_key}"
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.8,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 1000
            }
        }

        try:
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                logger.error(
                    f"Gemini API Error {response.status_code}: {response.text}"
                )
                return self._fallback_dna(product_name, offer)

            result = response.json()

            if "candidates" not in result:
                logger.error(result)
                return self._fallback_dna(product_name, offer)

            text = result["candidates"][0]["content"]["parts"][0]["text"]

            # Remove markdown formatting if Gemini returns it
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            try:
                return json.loads(text)

            except json.JSONDecodeError:
                logger.warning(
                    "Gemini returned non-JSON output. Returning wrapped response."
                )

                return {
                    "hook": text[:80],
                    "value_prop": offer,
                    "cta": "Shop Now",
                    "visual_sentiment": "Modern lifestyle product photography"
                }

        except requests.exceptions.Timeout:
            logger.error("Gemini request timed out.")
            return self._fallback_dna(product_name, offer)

        except Exception as e:
            logger.exception(e)
            return self._fallback_dna(product_name, offer)

    def _fallback_dna(self, product_name, offer):
        return {
            "hook": f"Discover the Best {product_name}",
            "value_prop": offer,
            "cta": "Shop Now",
            "visual_sentiment": (
                "Modern, clean lifestyle photography with warm lighting"
            )
        }