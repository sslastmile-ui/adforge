"""Runbook - Verified runbooks for common errors.""" 
 
class Runbook: 
    def __init__(self): 
        self.runbooks = { 
            "timeout": {"steps": ["Increase timeout", "Retry with backoff"]}, 
            "authentication": {"steps": ["Check API key", "Refresh token"]}, 
            "rate_limit": {"steps": ["Reduce request rate", "Wait 60s"]} 
        } 
 
    async def get_runbook(self, error_type): 
        return self.runbooks.get(error_type, {"steps": ["Unknown error", "Escalate to human"]}) 
