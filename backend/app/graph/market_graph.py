"""Local Market Graph - Connect people, businesses, locations, events.""" 
 
class MarketGraph: 
    def __init__(self): 
        self.nodes = [] 
        self.edges = [] 
 
    def add_node(self, node_type, data): 
        """Add a node to the graph.""" 
        self.nodes.append({"type": node_type, "data": data}) 
 
    def add_edge(self, source, target, relationship): 
        """Add an edge between nodes.""" 
        self.edges.append({"source": source, "target": target, "relationship": relationship}) 
 
    def find_connections(self, node_id, depth=2): 
        """Find connections to a specific node.""" 
        connections = [] 
        for edge in self.edges: 
            if edge["source"] == node_id or edge["target"] == node_id: 
                connections.append(edge) 
        return connections 
