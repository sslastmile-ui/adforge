"""CEO Constitution - Business goals, brand rules, agent authority.""" 
 
class CEOConstitution: 
    def __init__(self): 
        self.rules = { 
            "brand_voice": "Professional", 
            "max_discount": 50, 
            "approval_required": ["PUBLISH", "DELETE", "FINANCIAL"] 
        } 
 
    async def check_authority(self, action): 
        if action in self.rules["approval_required"]: 
            return {"allowed": False, "reason": f"Approval required for {action}"} 
        return {"allowed": True, "reason": "Action permitted"} 
