"""CEO Constitution - Business goals, brand rules, agent authority.""" 
 
class CEOConstitution: 
    def __init__(self, tenant_id): 
        self.tenant_id = tenant_id 
        self.rules = { 
            "brand_voice": "Professional", 
            "max_discount": 50, 
            "approval_required": ["PUBLISH", "DELETE", "FINANCIAL/REFUND"], 
            "never_actions": ["Delete tenant data", "Modify payment info"], 
            "permissions": { 
                "READ": {"agents": ["CEO", "CMO", "CFO"]}, 
                "CREATE": {"agents": ["CMO", "COO"]}, 
                "UPDATE": {"agents": ["CMO", "COO", "CFO"]}, 
                "PUBLISH": {"agents": ["CMO"], "requires_approval": True}, 
                "DELETE": {"agents": ["CEO"], "requires_approval": True}, 
                "SPEND": {"agents": ["CMO", "CFO"], "requires_approval": True}, 
                "CONTACT": {"agents": ["Sales Director", "Customer Success"]}, 
                "FINANCIAL/REFUND": {"agents": ["CFO"], "requires_approval": True}, 
                "APPROVE": {"agents": ["CEO", "CFO"]}, 
                "ESCALATE": {"agents": ["CEO"]} 
            } 
        } 
 
    async def check_authority(self, action, agent): 
        if action in self.rules["never_actions"]: 
            return {"allowed": False, "reason": "Action is never allowed"} 
        if action in self.rules["approval_required"]: 
            return {"allowed": True, "requires_approval": True} 
        if agent in self.rules["permissions"].get(action, {}).get("agents", []): 
            return {"allowed": True, "requires_approval": False} 
        return {"allowed": False, "reason": f"Agent {agent} not authorized for {action}"} 
