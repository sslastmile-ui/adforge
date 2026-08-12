from typing import Dict, List, Optional
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class RealEstateService:
    def __init__(self):
        self.properties = {}
        self.listings = {}
        self.enquiries = {}
        self.visits = {}
    
    def create_property(self, data: Dict) -> Dict:
        property_id = str(uuid.uuid4())
        self.properties[property_id] = {"id": property_id, **data, "created_at": datetime.utcnow().isoformat(), "status": "draft", "verification_status": "pending"}
        return self.properties[property_id]
    
    def get_property(self, property_id: str) -> Optional[Dict]:
        return self.properties.get(property_id)
    
    def list_properties(self, filters: Optional[Dict] = None) -> List[Dict]:
        properties = list(self.properties.values())
        if filters:
            for key, value in filters.items():
                properties = [p for p in properties if p.get(key) == value]
        return properties
    
    def create_listing(self, property_id: str, listing_type: str, price: float, details: Dict) -> Dict:
        if property_id not in self.properties:
            return {"error": "Property not found"}
        listing_id = str(uuid.uuid4())
        self.listings[listing_id] = {"id": listing_id, "property_id": property_id, "type": listing_type, "price": price, "details": details, "status": "active", "created_at": datetime.utcnow().isoformat()}
        return self.listings[listing_id]
    
    def get_listing(self, listing_id: str) -> Optional[Dict]:
        return self.listings.get(listing_id)
    
    def create_enquiry(self, listing_id: str, customer_id: str, message: str) -> Dict:
        if listing_id not in self.listings:
            return {"error": "Listing not found"}
        enquiry_id = str(uuid.uuid4())
        self.enquiries[enquiry_id] = {"id": enquiry_id, "listing_id": listing_id, "customer_id": customer_id, "message": message, "status": "new", "created_at": datetime.utcnow().isoformat()}
        return self.enquiries[enquiry_id]
    
    def schedule_visit(self, enquiry_id: str, visit_date: str, visit_time: str) -> Dict:
        if enquiry_id not in self.enquiries:
            return {"error": "Enquiry not found"}
        visit_id = str(uuid.uuid4())
        self.visits[visit_id] = {"id": visit_id, "enquiry_id": enquiry_id, "visit_date": visit_date, "visit_time": visit_time, "status": "scheduled", "created_at": datetime.utcnow().isoformat()}
        return self.visits[visit_id]
    
    def update_visit_outcome(self, visit_id: str, outcome: str, notes: str) -> bool:
        if visit_id not in self.visits:
            return False
        self.visits[visit_id]["outcome"] = outcome
        self.visits[visit_id]["notes"] = notes
        self.visits[visit_id]["status"] = "completed"
        return True
    
    def get_statistics(self) -> Dict:
        return {"total_properties": len(self.properties), "active_listings": len([l for l in self.listings.values() if l["status"] == "active"]), "total_enquiries": len(self.enquiries), "total_visits": len(self.visits), "visit_completed": len([v for v in self.visits.values() if v["status"] == "completed"])}