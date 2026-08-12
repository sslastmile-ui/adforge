"""AIIncident - Track and manage AI incidents.""" 
 
from datetime import datetime 
import uuid 
 
class AIIncident: 
    def __init__(self, provider, capability, error_message): 
        self.id = str(uuid.uuid4()) 
        self.provider = provider 
        self.capability = capability 
        self.error_message = error_message 
        self.status = "open" 
        self.created_at = datetime.utcnow().isoformat() 
        self.resolution = None 
 
    def resolve(self, resolution): 
        self.status = "resolved" 
        self.resolution = resolution 
        self.resolved_at = datetime.utcnow().isoformat() 
