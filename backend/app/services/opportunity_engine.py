"""Opportunity Engine - Turns signals into campaign opportunities.""" 
 
class OpportunityEngine: 
    def __init__(self): 
        self.opportunities = [] 
 
    async def detect_opportunities(self, signals): 
        """Detect opportunities from signals.""" 
        for signal in signals: 
            if signal.get("type") == "demand" and signal.get("data", {}).get("volume", 0) 
                self.opportunities.append({ 
                    "type": "demand_spike", 
                    "description": f"High demand detected", 
                    "confidence": 0.8 
                }) 
        return self.opportunities 
