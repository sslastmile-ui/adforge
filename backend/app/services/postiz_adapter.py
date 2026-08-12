import os
import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PostizAdapter:
    def __init__(self):
        self.api_url = os.getenv("POSTIZ_API_URL", "https://api.postiz.com")
        self.api_key = os.getenv("POSTIZ_API_KEY")
        self.workspace_id = os.getenv("POSTIZ_WORKSPACE_ID")
        
    async def schedule_post(self, content: str, platforms: List[str], scheduled_at: Optional[str] = None, media_urls: Optional[List[str]] = None, tenant_id: Optional[str] = None) -> Dict:
        if not self.api_key:
            return {"error": "Postiz not configured"}
        payload = {"workspaceId": self.workspace_id, "content": content, "platforms": platforms, "scheduledAt": scheduled_at or datetime.utcnow().isoformat(), "mediaUrls": media_urls or []}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            response = requests.post(f"{self.api_url}/api/v1/posts", json=payload, headers=headers)
            if response.status_code == 200:
                return {"success": True, "post_id": response.json().get("id"), "scheduled_at": scheduled_at}
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            logger.error(f"Postiz schedule failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_post_status(self, post_id: str) -> Dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(f"{self.api_url}/api/v1/posts/{post_id}", headers=headers)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def get_connected_accounts(self) -> List[Dict]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(f"{self.api_url}/api/v1/accounts", headers=headers)
            return response.json().get("accounts", [])
        except Exception as e:
            logger.error(f"Failed to get connected accounts: {e}")
            return []
    
    async def cancel_scheduled_post(self, post_id: str) -> Dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.delete(f"{self.api_url}/api/v1/posts/{post_id}", headers=headers)
            return {"success": response.status_code == 200}
        except Exception as e:
            return {"success": False, "error": str(e)}