import logging
from typing import Dict, List, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class ConnectorFabric:
    def __init__(self):
        self.connectors = {}
        self.connections = {}
    
    def register_connector(self, name: str, connector_config: Dict) -> bool:
        if name in self.connectors:
            logger.warning(f"Connector {name} already registered")
            return False
        self.connectors[name] = {"name": name, "config": connector_config, "registered_at": datetime.utcnow().isoformat(), "status": "active"}
        logger.info(f"Connector {name} registered successfully")
        return True
    
    def get_connector(self, name: str) -> Optional[Dict]:
        return self.connectors.get(name)
    
    def list_connectors(self) -> List[str]:
        return list(self.connectors.keys())
    
    def connect(self, connector_name: str, credentials: Dict) -> Dict:
        if connector_name not in self.connectors:
            return {"success": False, "error": f"Connector {connector_name} not found"}
        connection_id = str(uuid.uuid4())
        self.connections[connection_id] = {"connector": connector_name, "credentials": "redacted", "connected_at": datetime.utcnow().isoformat(), "status": "active"}
        return {"success": True, "connection_id": connection_id, "status": "active"}
    
    def disconnect(self, connection_id: str) -> Dict:
        if connection_id not in self.connections:
            return {"success": False, "error": "Connection not found"}
        self.connections[connection_id]["status"] = "disconnected"
        return {"success": True, "message": "Disconnected successfully"}
    
    def get_connection_status(self, connection_id: str) -> Dict:
        return self.connections.get(connection_id, {"error": "Connection not found"})
    
    def get_metrics(self) -> Dict:
        return {"total_connectors": len(self.connectors), "active_connections": len([c for c in self.connections.values() if c.get("status") == "active"]), "total_connections": len(self.connections)}