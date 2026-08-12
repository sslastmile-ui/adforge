import logging
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import hashlib

logger = logging.getLogger(__name__)

class ErrorIntelligence:
    def __init__(self):
        self.incidents = {}
        self.patterns = {}
        self.resolutions = {}
    
    def record_incident(self, error: str, provider: str, capability: str, context: Dict) -> str:
        incident_id = str(uuid.uuid4())
        fingerprint = hashlib.md5(f"{error}{provider}{capability}".encode()).hexdigest()
        self.incidents[incident_id] = {"id": incident_id, "error": error, "provider": provider, "capability": capability, "fingerprint": fingerprint, "context": context, "attempts": 1, "status": "new", "created_at": datetime.utcnow().isoformat()}
        if fingerprint not in self.patterns:
            self.patterns[fingerprint] = {"fingerprint": fingerprint, "occurrences": 0, "first_seen": datetime.utcnow().isoformat(), "last_seen": datetime.utcnow().isoformat(), "providers": []}
        self.patterns[fingerprint]["occurrences"] += 1
        self.patterns[fingerprint]["last_seen"] = datetime.utcnow().isoformat()
        if provider not in self.patterns[fingerprint]["providers"]:
            self.patterns[fingerprint]["providers"].append(provider)
        return incident_id
    
    def get_pattern(self, fingerprint: str) -> Optional[Dict]:
        return self.patterns.get(fingerprint)
    
    def get_incident(self, incident_id: str) -> Optional[Dict]:
        return self.incidents.get(incident_id)
    
    def add_resolution(self, fingerprint: str, resolution: str, verified: bool = False) -> bool:
        if fingerprint not in self.resolutions:
            self.resolutions[fingerprint] = {"fingerprint": fingerprint, "resolutions": [], "verified": verified, "created_at": datetime.utcnow().isoformat()}
        self.resolutions[fingerprint]["resolutions"].append({"resolution": resolution, "timestamp": datetime.utcnow().isoformat()})
        if verified:
            self.resolutions[fingerprint]["verified"] = True
        return True
    
    def get_resolution(self, fingerprint: str) -> Optional[Dict]:
        return self.resolutions.get(fingerprint)
    
    def get_statistics(self) -> Dict:
        return {"total_incidents": len(self.incidents), "total_patterns": len(self.patterns), "total_resolutions": len(self.resolutions), "unique_fingerprints": len(self.patterns)}