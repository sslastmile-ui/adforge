"""AIIncidentPattern - Detect patterns in incidents.""" 
 
class AIIncidentPattern: 
    def __init__(self): 
        self.patterns = [] 
 
    def detect_patterns(self, incidents): 
        """Detect common patterns in incidents.""" 
        pattern_counts = {} 
        for incident in incidents: 
            key = f"{incident.provider}_{incident.capability}" 
            pattern_counts[key] = pattern_counts.get(key, 0) + 1 
        return [{"pattern": k, "count": v} for k, v in pattern_counts.items() if v 
