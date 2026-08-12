"""OAuth Manager - OAuth token management for connectors.""" 
 
class OAuthManager: 
    def __init__(self): 
        self.tokens = {} 
 
    async def get_token(self, connector): 
        token = self.tokens.get(connector, {}).get("access_token") 
        return {"connector": connector, "token": token, "valid": token is not None} 
