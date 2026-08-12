"""Audit Manager - Auditing every connector action.""" 
 
from datetime import datetime 
 
class AuditManager: 
    def __init__(self): 
        self.audits = [] 
 
    async def log_action(self, connector, action, user, details): 
        self.audits.append({ 
            "connector": connector, 
            "action": action, 
            "user": user, 
            "details": details, 
            "timestamp": datetime.utcnow().isoformat() 
        }) 
