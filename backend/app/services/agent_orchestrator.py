import logging
from typing import Dict, List, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    def __init__(self):
        self.agents = {}
        self.jobs = {}
        self.running_tasks = 0
        self.completed_tasks = 0
        self.failed_tasks = 0
    
    def register_agent(self, name: str, agent_instance) -> bool:
        self.agents[name] = agent_instance
        logger.info(f"Agent {name} registered successfully")
        return True
    
    def get_agent(self, name: str):
        return self.agents.get(name)
    
    async def dispatch_task(self, agent_name: str, task: str, data: Dict) -> Dict:
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {"agent": agent_name, "task": task, "data": data, "status": "queued", "created_at": datetime.utcnow().isoformat()}
        self.running_tasks += 1
        agent = self.get_agent(agent_name)
        if not agent:
            self.failed_tasks += 1
            return {"error": f"Agent {agent_name} not found", "job_id": job_id}
        try:
            result = await agent.execute(task, data)
            self.jobs[job_id]["status"] = "completed"
            self.jobs[job_id]["result"] = result
            self.completed_tasks += 1
            return {"success": True, "job_id": job_id, "result": result}
        except Exception as e:
            self.jobs[job_id]["status"] = "failed"
            self.jobs[job_id]["error"] = str(e)
            self.failed_tasks += 1
            logger.error(f"Task {task} for agent {agent_name} failed: {e}")
            return {"success": False, "job_id": job_id, "error": str(e)}
        finally:
            self.running_tasks -= 1
    
    def get_job_status(self, job_id: str) -> Dict:
        return self.jobs.get(job_id, {"error": "Job not found"})
    
    def get_metrics(self) -> Dict:
        return {"running_tasks": self.running_tasks, "completed_tasks": self.completed_tasks, "failed_tasks": self.failed_tasks, "total_jobs": len(self.jobs)}
    
    def list_agents(self) -> List[str]:
        return list(self.agents.keys())