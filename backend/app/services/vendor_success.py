from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta
import uuid

logger = logging.getLogger(__name__)

class VendorSuccess:
    def __init__(self):
        self.vendors = {}
        self.health_checks = {}
        self.milestones = {}
    
    def register_vendor(self, name: str, vendor_type: str, contact_email: str, metadata: Optional[Dict] = None) -> Dict:
        vendor_id = str(uuid.uuid4())
        self.vendors[vendor_id] = {"id": vendor_id, "name": name, "type": vendor_type, "contact_email": contact_email, "metadata": metadata or {}, "status": "onboarding", "created_at": datetime.utcnow().isoformat(), "health_score": 0, "days_active": 0, "last_activity": datetime.utcnow().isoformat()}
        return self.vendors[vendor_id]
    
    def get_vendor(self, vendor_id: str) -> Optional[Dict]:
        return self.vendors.get(vendor_id)
    
    def update_health(self, vendor_id: str, score: int, metrics: Dict) -> bool:
        if vendor_id not in self.vendors:
            return False
        self.vendors[vendor_id]["health_score"] = score
        self.vendors[vendor_id]["last_activity"] = datetime.utcnow().isoformat()
        self.health_checks[vendor_id] = {"score": score, "metrics": metrics, "timestamp": datetime.utcnow().isoformat()}
        return True
    
    def get_health(self, vendor_id: str) -> Optional[Dict]:
        if vendor_id not in self.vendors:
            return None
        return {"health_score": self.vendors[vendor_id]["health_score"], "status": self.vendors[vendor_id]["status"], "last_activity": self.vendors[vendor_id]["last_activity"]}
    
    def add_milestone(self, vendor_id: str, milestone: str, details: Dict) -> bool:
        if vendor_id not in self.vendors:
            return False
        if vendor_id not in self.milestones:
            self.milestones[vendor_id] = []
        self.milestones[vendor_id].append({"milestone": milestone, "details": details, "achieved_at": datetime.utcnow().isoformat()})
        self.vendors[vendor_id]["days_active"] = (datetime.utcnow() - datetime.fromisoformat(self.vendors[vendor_id]["created_at"])).days
        return True
    
    def get_milestones(self, vendor_id: str) -> List[Dict]:
        return self.milestones.get(vendor_id, [])
    
    def calculate_health_score(self, vendor_id: str) -> float:
        if vendor_id not in self.vendors:
            return 0.0
        health = 0.0
        if self.vendors[vendor_id]["days_active"] > 30:
            health += 0.2
        if self.vendors[vendor_id]["health_score"] > 50:
            health += 0.3
        if self.vendors[vendor_id]["status"] == "active":
            health += 0.3
        if len(self.get_milestones(vendor_id)) > 3:
            health += 0.2
        return min(health, 1.0)
    
    def get_statistics(self) -> Dict:
        return {"total_vendors": len(self.vendors), "active_vendors": len([v for v in self.vendors.values() if v["status"] == "active"]), "onboarding_vendors": len([v for v in self.vendors.values() if v["status"] == "onboarding"]), "avg_health": sum([v["health_score"] for v in self.vendors.values()]) / len(self.vendors) if self.vendors else 0}