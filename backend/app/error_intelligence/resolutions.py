"""AIResolution - Store and reuse resolutions.""" 
 
class AIResolution: 
    def __init__(self): 
        self.resolutions = [] 
 
    def add_resolution(self, incident_id, solution, verified=False): 
        self.resolutions.append({ 
            "incident_id": incident_id, 
            "solution": solution, 
            "verified": verified 
        }) 
 
    def find_solution(self, incident): 
        for resolution in self.resolutions: 
            if resolution["verified"]: 
                return resolution["solution"] 
        return None 
