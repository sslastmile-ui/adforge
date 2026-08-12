"""A/B Testing Service - Test hooks, creatives, offers, CTAs, landing pages.""" 
 
class ABTestingService: 
    def __init__(self): 
        self.tests = [] 
 
    async def create_test(self, name, variants): 
        test = {"name": name, "variants": variants, "results": {}} 
        self.tests.append(test) 
        return test 
