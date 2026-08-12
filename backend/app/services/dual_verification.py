import os 
import logging 
import secrets 
from typing import Dict, Optional, List 
from datetime import datetime, timedelta 
import uuid 
 
logger = logging.getLogger(__name__) 
 
class DualVerificationService: 
    def __init__(self): 
        self.otp_store = {} 
        self.verified_contacts = {} 
        self.contact_disclosures = {} 
        self.vendor_lead_contacts = {} 
        self.audit_logs = [] 
        self.otp_ttl = 300 
        self.max_otp_attempts = 5 
 
    def _mask_phone(self, phone: str) -
        if not phone or len(phone) < 10: 
            return "***" 
        return f"{phone[:2]}****{phone[-2:]}" 
 
    async def request_otp(self, phone: str, customer_id: Optional[str] = None) -
        otp = f"{secrets.randbelow(1000000):06d}" 
        self.otp_store[phone] = { 
            "otp": otp, 
            "expires_at": (datetime.utcnow() + timedelta(seconds=self.otp_ttl)).isoformat(), 
            "verified": False, 
            "attempts": 0, 
            "customer_id": customer_id 
        } 
        logger.info(f"OTP requested for {self._mask_phone(phone)}") 
        return { 
            "success": True, 
            "message": "OTP sent successfully", 
            "otp": otp, 
            "expires_in": self.otp_ttl, 
            "phone_masked": self._mask_phone(phone) 
        } 
 
    async def verify_otp(self, phone: str, otp: str) -
        if phone not in self.otp_store: 
            return {"success": False, "error": "No OTP requested for this number"} 
        record = self.otp_store[phone] 
        if record["verified"]: 
            return {"success": False, "error": "OTP already verified"} 
        if datetime.fromisoformat(record["expires_at"]) < datetime.utcnow(): 
            return {"success": False, "error": "OTP has expired"} 
        record["attempts"] += 1 
        if record["attempts"] 
            return {"success": False, "error": "Maximum attempts exceeded"} 
        if record["otp"] != otp: 
            return {"success": False, "error": "Invalid OTP"} 
        record["verified"] = True 
        customer_id = record.get("customer_id") 
        if customer_id: 
            self.verified_contacts[customer_id] = { 
                "phone": phone, 
                "verified_at": datetime.utcnow().isoformat(), 
                "method": "otp_login" 
            } 
            logger.info(f"Phone verified via OTP for customer {customer_id}") 
        return {"success": True, "message": "Phone verified successfully", "customer_id": customer_id} 
 
    async def get_verified_contact(self, customer_id: str) -
        return self.verified_contacts.get(customer_id) 
 
    async def request_share_contact(self, customer_id: str, vendor_id: str, context: str, purpose: str) -
        verified = await self.get_verified_contact(customer_id) 
        if verified: 
            return { 
                "requires_otp": False, 
                "verified": True, 
                "phone_masked": self._mask_phone(verified["phone"]), 
                "vendor_id": vendor_id, 
                "customer_id": customer_id, 
                "context": context, 
                "purpose": purpose 
            } 
        return { 
            "requires_otp": True, 
            "verified": False, 
            "vendor_id": vendor_id, 
            "customer_id": customer_id, 
            "context": context, 
            "purpose": purpose 
        } 
 
    async def confirm_disclosure(self, customer_id: str, vendor_id: str, context_id: str, purpose: str) -
        verified = await self.get_verified_contact(customer_id) 
        if not verified: 
            return {"success": False, "error": "No verified contact found"} 
        disclosure_id = str(uuid.uuid4()) 
        self.contact_disclosures[disclosure_id] = { 
            "disclosure_id": disclosure_id, 
            "customer_id": customer_id, 
            "vendor_id": vendor_id, 
            "context_id": context_id, 
            "contact_id": verified["phone"], 
            "purpose": purpose, 
            "consent_state": "confirmed", 
            "created_at": datetime.utcnow().isoformat(), 
            "revoked_at": None 
        } 
        lead_id = str(uuid.uuid4()) 
        self.vendor_lead_contacts[lead_id] = { 
            "lead_id": lead_id, 
            "vendor_id": vendor_id, 
            "customer_id": customer_id, 
            "disclosed_contact_id": verified["phone"], 
            "disclosure_id": disclosure_id, 
            "received_at": datetime.utcnow().isoformat(), 
            "usage_purpose": purpose 
        } 
        self._audit("contact_disclosed", customer_id, vendor_id, disclosure_id) 
        return { 
            "success": True, 
            "disclosure_id": disclosure_id, 
            "lead_id": lead_id, 
            "phone": verified["phone"], 
            "vendor_id": vendor_id 
        } 
 
    async def revoke_disclosure(self, disclosure_id: str) -
        if disclosure_id not in self.contact_disclosures: 
            return {"success": False, "error": "Disclosure not found"} 
        self.contact_disclosures[disclosure_id]["revoked_at"] = datetime.utcnow().isoformat() 
        self.contact_disclosures[disclosure_id]["consent_state"] = "revoked" 
        self._audit("contact_revoked", disclosure_id, None, disclosure_id) 
        return {"success": True, "message": "Disclosure revoked"} 
 
    def _audit(self, action: str, actor_id: str, target_id: str, resource_id: str): 
        self.audit_logs.append({ 
            "action": action, 
            "actor_id": actor_id, 
            "target_id": target_id, 
            "resource_id": resource_id, 
            "timestamp": datetime.utcnow().isoformat() 
        }) 
 
    def get_audit_logs(self, customer_id: Optional[str] = None, vendor_id: Optional[str] = None) -
        logs = self.audit_logs 
        if customer_id: 
            logs = [l for l in logs if l["actor_id"] == customer_id or l["target_id"] == customer_id] 
        if vendor_id: 
            logs = [l for l in logs if l["actor_id"] == vendor_id or l["target_id"] == vendor_id] 
        return logs 
 
    def get_statistics(self) -
        return { 
            "total_verified": len(self.verified_contacts), 
            "total_disclosures": len(self.contact_disclosures), 
            "total_leads": len(self.vendor_lead_contacts), 
            "total_audits": len(self.audit_logs) 
        } 
