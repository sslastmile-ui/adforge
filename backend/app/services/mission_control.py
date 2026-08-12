"""Mission Control - Live CEO/COO status, tasks, approvals, opportunities.""" 
 
class MissionControl: 
    def __init__(self): 
        self.agents = {} 
        self.tasks = [] 
        self.approvals = [] 
        self.opportunities = [] 
        self.kpi_warnings = [] 
        self.provider_failures = [] 
 
    async def register_agent(self, agent_name, status): 
        self.agents[agent_name] = {"status": status, "last_active": "now"} 
 
    async def add_task(self, task): 
        task["status"] = "queued" 
        self.tasks.append(task) 
 
    async def get_status(self): 
        running = len([t for t in self.tasks if t["status"] == "running"]) 
        completed = len([t for t in self.tasks if t["status"] == "completed"]) 
        waiting = len([t for t in self.tasks if t["status"] == "waiting"]) 
        failed = len([t for t in self.tasks if t["status"] == "failed"]) 
        return { 
            "agents": self.agents, 
            "tasks": {"running": running, "completed": completed, "waiting": waiting, "failed": failed}, 
            "approvals": len(self.approvals), 
            "opportunities": len(self.opportunities), 
            "kpi_warnings": self.kpi_warnings, 
            "provider_failures": self.provider_failures 
        } 
