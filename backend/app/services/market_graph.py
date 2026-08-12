from typing import Dict, List, Optional, Set
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class MarketGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.node_types = ["business", "customer", "location", "event", "offer", "property", "review", "order"]
    
    def add_node(self, node_id: str, node_type: str, properties: Dict) -> bool:
        if node_type not in self.node_types:
            logger.warning(f"Invalid node type: {node_type}")
            return False
        self.nodes[node_id] = {"id": node_id, "type": node_type, "properties": properties, "created_at": datetime.utcnow().isoformat()}
        return True
    
    def get_node(self, node_id: str) -> Optional[Dict]:
        return self.nodes.get(node_id)
    
    def add_edge(self, from_node: str, to_node: str, edge_type: str, properties: Dict) -> bool:
        if from_node not in self.nodes or to_node not in self.nodes:
            logger.warning("One or both nodes not found")
            return False
        edge_id = str(uuid.uuid4())
        self.edges[edge_id] = {"from": from_node, "to": to_node, "type": edge_type, "properties": properties, "created_at": datetime.utcnow().isoformat()}
        return True
    
    def get_neighbors(self, node_id: str, edge_type: Optional[str] = None) -> List[Dict]:
        neighbors = []
        for edge in self.edges.values():
            if edge["from"] == node_id:
                if edge_type is None or edge["type"] == edge_type:
                    neighbors.append(self.nodes.get(edge["to"]))
            if edge["to"] == node_id:
                if edge_type is None or edge["type"] == edge_type:
                    neighbors.append(self.nodes.get(edge["from"]))
        return [n for n in neighbors if n is not None]
    
    def find_path(self, from_node: str, to_node: str, max_depth: int = 5) -> Optional[List[str]]:
        if from_node not in self.nodes or to_node not in self.nodes:
            return None
        visited = set()
        queue = [[from_node]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == to_node:
                return path
            if len(path) >= max_depth:
                continue
            for neighbor in self.get_neighbors(node):
                if neighbor["id"] not in visited:
                    visited.add(neighbor["id"])
                    new_path = list(path)
                    new_path.append(neighbor["id"])
                    queue.append(new_path)
        return None
    
    def get_statistics(self) -> Dict:
        return {"total_nodes": len(self.nodes), "total_edges": len(self.edges), "node_types": {t: len([n for n in self.nodes.values() if n["type"] == t]) for t in self.node_types}}