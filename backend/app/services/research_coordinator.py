"""Research Coordinator - Coordinates Google/Instagram/Market researchers.""" 
 
from ..agents.google_researcher import GoogleResearcher 
from ..agents.instagram_researcher import InstagramResearcher 
from ..agents.market_researcher import MarketResearcher 
 
class ResearchCoordinator: 
    def __init__(self): 
        self.researchers = { 
            "google": GoogleResearcher(), 
            "instagram": InstagramResearcher(), 
            "market": MarketResearcher() 
        } 
 
    async def research_all(self, query): 
        results = {} 
        for name, researcher in self.researchers.items(): 
            results[name] = await researcher.research(query) 
        return {"query": query, "results": results} 
