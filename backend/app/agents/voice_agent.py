"""Voice Agent - Voice, transcript, intent, action and handoff.""" 
 
class VoiceAgent: 
    def __init__(self): 
        self.name = "Voice Agent" 
 
    async def process_voice(self, transcript): 
        return {"intent": "booking", "action": "schedule", "handoff": False, "agent": "Voice Agent"} 
