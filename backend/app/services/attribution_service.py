"""Attribution Service - Customer journey attribution.""" 
 
class AttributionService: 
    def __init__(self): 
        self.model = "last_click" 
 
    def calculate_attribution(self, events): 
        """Calculate attribution using last-click model.""" 
        if not events: 
            return {} 
        last = events[-1] 
        return {last.get("channel", "unknown"): 1.0} 
