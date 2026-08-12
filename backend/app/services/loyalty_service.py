"""Loyalty Service - Manage rewards, stamps, repeat visits.""" 
 
class LoyaltyService: 
    def __init__(self): 
        self.records = {} 
 
    def add_points(self, customer_id, points): 
        if customer_id not in self.records: 
            self.records[customer_id] = {"points": 0, "stamps": 0, "tier": "bronze"} 
        self.records[customer_id]["points"] += points 
        return self.records[customer_id] 
