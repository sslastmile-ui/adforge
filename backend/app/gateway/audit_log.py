"""Audit Log - Logging every provider switch.""" 
 
from datetime import datetime 
 
class AuditLog: 
    def __init__(self): 
        self.entries = [] 
 
    async def log_switch(self, from_provider, to_provider, reason): 
        self.entries.append({ 
            "from": from_provider, 
            "to": to_provider, 
            "reason": reason, 
            "timestamp": datetime.utcnow().isoformat() 
        }) 
