from typing import Dict, List, Optional 
from datetime import datetime 
import uuid 
import logging 
 
logger = logging.getLogger(__name__) 
 
class DeveloperPackage: 
    def __init__(self, package_id: str, name: str, description: str, dependencies: List[str] = None): 
        self.package_id = package_id 
        self.name = name 
        self.description = description 
        self.dependencies = dependencies or [] 
        self.status = "pending" 
        self.owner = None 
        self.contracts = [] 
        self.tests = [] 
        self.mocks = [] 
        self.migrations = [] 
        self.created_at = datetime.utcnow().isoformat() 
        self.updated_at = datetime.utcnow().isoformat() 
 
class DeveloperPackManager: 
    def __init__(self): 
        self.packages = {} 
        self.integration_runs = [] 
        self._initialize_packages() 
 
    def _initialize_packages(self): 
        packages = [ 
            {"id": "D01", "name": "Platform Foundation", "deps": []}, 
            {"id": "D02", "name": "Identity, OTP, Customer 360", "deps": ["D01"]}, 
            {"id": "D03", "name": "Vendor OS, Onboarding", "deps": ["D01"]}, 
            {"id": "D04", "name": "Customer App, Discovery", "deps": ["D01", "D02", "D03"]}, 
            {"id": "D05", "name": "Restaurant & Order", "deps": ["D03", "D04"]}, 
            {"id": "D06", "name": "Real Estate Vertical", "deps": ["D03", "D04"]}, 
            {"id": "D07", "name": "Booking, Ride, Invoice", "deps": ["D02", "D03"]}, 
            {"id": "D08", "name": "AI Chat, Voice, Call Bridge", "deps": ["D02", "D03"]}, 
            {"id": "D09", "name": "AI Gateway, Provider Fabric", "deps": ["D01"]}, 
            {"id": "D10", "name": "Marketing OS, AdForge", "deps": ["D03", "D04"]}, 
            {"id": "D11", "name": "Sourcing AI, Research", "deps": ["D03", "D09"]}, 
            {"id": "D12", "name": "AI Workforce", "deps": ["D01", "D09"]}, 
            {"id": "D13", "name": "Connector Fabric, MCP", "deps": ["D09"]}, 
            {"id": "D14", "name": "Reliability, Observability", "deps": ["D01"]}, 
            {"id": "D15", "name": "Infrastructure, CI/CD", "deps": ["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "D11", "D12", "D13", "D14"]} 
        ] 
        for pkg in packages: 
            self.packages[pkg["id"]] = DeveloperPackage(pkg["id"], pkg["name"], f"Package {pkg['id']}", pkg["deps"]) 
 
    def get_package(self, package_id: str) -
        return self.packages.get(package_id) 
 
    def list_packages(self) -
        return [{"id": p.package_id, "name": p.name, "status": p.status, "deps": p.dependencies} for p in self.packages.values()] 
 
    def assign_owner(self, package_id: str, owner: str) -
        pkg = self.get_package(package_id) 
        if not pkg: 
            return False 
        pkg.owner = owner 
        pkg.updated_at = datetime.utcnow().isoformat() 
        return True 
 
    def add_contract(self, package_id: str, contract: str) -
        pkg = self.get_package(package_id) 
        if not pkg: 
            return False 
        pkg.contracts.append({"contract": contract, "added_at": datetime.utcnow().isoformat()}) 
        pkg.updated_at = datetime.utcnow().isoformat() 
        return True 
 
    def add_test(self, package_id: str, test: str) -
        pkg = self.get_package(package_id) 
        if not pkg: 
            return False 
        pkg.tests.append({"test": test, "added_at": datetime.utcnow().isoformat()}) 
        pkg.updated_at = datetime.utcnow().isoformat() 
        return True 
 
    def get_assembly_order(self) -
        ordered = [] 
        visited = set() 
        def visit(pkg_id): 
            if pkg_id in visited: 
                return 
            visited.add(pkg_id) 
            pkg = self.get_package(pkg_id) 
            if pkg: 
                for dep in pkg.dependencies: 
                    visit(dep) 
                if pkg_id not in ordered: 
                    ordered.append(pkg_id) 
        for pkg_id in self.packages: 
            visit(pkg_id) 
        return ordered 
 
    def get_statistics(self) -
        total = len(self.packages) 
        completed = len([p for p in self.packages.values() if p.status == "completed"]) 
        in_progress = len([p for p in self.packages.values() if p.status == "in_progress"]) 
        pending = len([p for p in self.packages.values() if p.status == "pending"]) 
        return {"total_packages": total, "completed": completed, "in_progress": in_progress, "pending": pending, "assembly_order": self.get_assembly_order()} 
