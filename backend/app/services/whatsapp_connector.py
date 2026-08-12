import os
import json
import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class WhatsAppConnector:
    def __init__(self):
        self.api_version = "v18.0"
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.webhook_verify_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN")
        
    async def send_message(self, to: str, message: str, message_type: str = "text", tenant_id: Optional[str] = None) -> Dict:
        if not self.phone_number_id or not self.access_token:
            return {"error": "WhatsApp not configured"}
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": message}}
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        try:
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            if response.status_code == 200:
                return {"success": True, "message_id": result.get("messages", [{}])[0].get("id"), "timestamp": datetime.utcnow().isoformat()}
            else:
                logger.error(f"WhatsApp API error: {result}")
                return {"success": False, "error": result}
        except Exception as e:
            logger.error(f"WhatsApp send failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_template(self, to: str, template_name: str, language: str = "en", components: Optional[List[Dict]] = None) -> Dict:
        if not self.phone_number_id or not self.access_token:
            return {"error": "WhatsApp not configured"}
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        payload = {"messaging_product": "whatsapp", "to": to, "type": "template", "template": {"name": template_name, "language": {"code": language}, "components": components or []}}
        headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        try:
            response = requests.post(url, json=payload, headers=headers)
            result = response.json()
            if response.status_code == 200:
                return {"success": True, "message_id": result.get("messages", [{}])[0].get("id")}
            else:
                return {"success": False, "error": result}
        except Exception as e:
            logger.error(f"WhatsApp template send failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_message_status(self, message_id: str) -> Dict:
        if not self.access_token:
            return {"error": "WhatsApp not configured"}
        url = f"{self.base_url}/{message_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def mark_as_read(self, message_id: str) -> Dict:
        if not self.phone_number_id or not self.access_token:
            return {"error": "WhatsApp not configured"}
        url = f"{self.base_url}/{self.phone_number_id}/messages/{message_id}/mark_as_read"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.post(url, headers=headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def verify_webhook(self, mode: str, token: str, challenge: str) -> Dict:
        if mode == "subscribe" and token == self.webhook_verify_token:
            return {"success": True, "challenge": challenge}
        return {"success": False, "error": "Invalid verification token"}