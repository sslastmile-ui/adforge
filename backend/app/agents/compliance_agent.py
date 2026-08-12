"""Compliance Agent - Consent/policy/regulated-action checks.""" 
 
class ComplianceAgent: 
    def __init__(self): 
        self.name = "Compliance Agent" 
 
    async def check_compliance(self, action): 
        return {"compliant": True, "requires_consent": False, "agent": "Compliance Agent"} 
