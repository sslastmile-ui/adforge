"""Sourcing Manager - Approved scrapers, directories, APIs and lead-generation tools.""" 
 
class SourcingManager: 
    def __init__(self): 
        self.sources = { 
            "google": {"enabled": True, "type": "api"}, 
            "linkedin": {"enabled": True, "type": "api"}, 
            "instagram": {"enabled": True, "type": "api"}, 
            "directories": {"enabled": True, "type": "scraper"} 
        } 
 
    async def source_leads(self, criteria): 
        leads = [] 
        for source, config in self.sources.items(): 
            if config["enabled"]: 
                leads.append({ 
                    "source": source, 
                    "name": f"Lead from {source}", 
                    "confidence": 0.8 
                }) 
        return leads 
