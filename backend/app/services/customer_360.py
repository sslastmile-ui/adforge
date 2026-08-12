from typing import Dict, List, Optional
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class Customer360:
    def __init__(self):
        self.customers = {}
        self.interactions = {}
        self.preferences = {}
    
    def create_customer(self, name: str, email: str, phone: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict:
        customer_id = str(uuid.uuid4())
        self.customers[customer_id] = {"id": customer_id, "name": name, "email": email, "phone": phone, "metadata": metadata or {}, "created_at": datetime.utcnow().isoformat(), "interaction_count": 0, "loyalty_points": 0, "tier": "bronze"}
        return self.customers[customer_id]
    
    def get_customer(self, customer_id: str) -> Optional[Dict]:
        return self.customers.get(customer_id)
    
    def update_customer(self, customer_id: str, updates: Dict) -> bool:
        if customer_id not in self.customers:
            return False
        for key, value in updates.items():
            if key in ["name", "email", "phone", "metadata"]:
                self.customers[customer_id][key] = value
        self.customers[customer_id]["updated_at"] = datetime.utcnow().isoformat()
        return True
    
    def add_interaction(self, customer_id: str, interaction_type: str, details: Dict) -> Dict:
        if customer_id not in self.customers:
            return {"error": "Customer not found"}
        interaction_id = str(uuid.uuid4())
        self.interactions[interaction_id] = {"id": interaction_id, "customer_id": customer_id, "type": interaction_type, "details": details, "created_at": datetime.utcnow().isoformat()}
        self.customers[customer_id]["interaction_count"] += 1
        return self.interactions[interaction_id]
    
    def get_interactions(self, customer_id: str) -> List[Dict]:
        return [i for i in self.interactions.values() if i["customer_id"] == customer_id]
    
    def set_preference(self, customer_id: str, key: str, value) -> bool:
        if customer_id not in self.customers:
            return False
        if customer_id not in self.preferences:
            self.preferences[customer_id] = {}
        self.preferences[customer_id][key] = value
        return True
    
    def get_preference(self, customer_id: str, key: str):
        return self.preferences.get(customer_id, {}).get(key)
    
    def get_all_preferences(self, customer_id: str) -> Dict:
        return self.preferences.get(customer_id, {})
    
    def add_loyalty_points(self, customer_id: str, points: int) -> Dict:
        if customer_id not in self.customers:
            return {"error": "Customer not found"}
        self.customers[customer_id]["loyalty_points"] += points
        if self.customers[customer_id]["loyalty_points"] >= 1000:
            self.customers[customer_id]["tier"] = "gold"
        elif self.customers[customer_id]["loyalty_points"] >= 500:
            self.customers[customer_id]["tier"] = "silver"
        return {"new_points": self.customers[customer_id]["loyalty_points"], "tier": self.customers[customer_id]["tier"]}
    
    def get_statistics(self) -> Dict:
        return {"total_customers": len(self.customers), "total_interactions": len(self.interactions), "tiers": {"bronze": len([c for c in self.customers.values() if c.get("tier") == "bronze"]), "silver": len([c for c in self.customers.values() if c.get("tier") == "silver"]), "gold": len([c for c in self.customers.values() if c.get("tier") == "gold"])}}