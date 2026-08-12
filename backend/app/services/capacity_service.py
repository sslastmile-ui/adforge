"""Capacity Service - Check capacity before campaigns.""" 
 
class CapacityService: 
    def __init__(self): 
        self.capacity = {} 
 
    def check_capacity(self, resource_type, required): 
        """Check if capacity is available.""" 
        available = self.capacity.get(resource_type, 0) 
        return {"available": available, "required": required, "sufficient": available 
