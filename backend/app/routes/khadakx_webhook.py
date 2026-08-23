import hmac
import hashlib
import os
from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import KhadakxEvent

router = APIRouter()

SECRET = os.environ.get("ADFORGE_WEBHOOK_SECRET", "")


def verify_signature(raw_body: bytes, signature_header: str) -> bool:
    if not SECRET:
        raise HTTPException(status_code=503, detail="ADFORGE_WEBHOOK_SECRET is not configured")
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    received = signature_header.split("=", 1)[1].strip()
    return hmac.compare_digest(expected, received)


@router.post("")
async def receive_khadakx_event(
    request: Request,
    x_khadakx_signature: str = Header(default=""),
    x_khadakx_event_id: str = Header(default=""),
    x_khadakx_contract_version: str = Header(default="1.3"),
    db: Session = Depends(get_db),
):
    raw_body = await request.body()
    if not verify_signature(raw_body, x_khadakx_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    if not x_khadakx_event_id:
        raise HTTPException(status_code=400, detail="Missing X-KhadakX-Event-Id header")

    existing = db.query(KhadakxEvent).filter(KhadakxEvent.event_id == x_khadakx_event_id).first()
    if existing:
        return {"received": True, "duplicate": True, "eventId": x_khadakx_event_id}

    try:
        import json

        payload = json.loads(raw_body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Body must be valid JSON")

    event_type = str(payload.get("eventType", "unknown"))
    business_id = str(payload.get("businessId", ""))

    record = KhadakxEvent(
        event_id=x_khadakx_event_id,
        event_type=event_type,
        business_id=business_id,
        contract_version=x_khadakx_contract_version or "1.3",
        payload=payload,
        received_at=datetime.utcnow(),
    )
    db.add(record)
    db.commit()

    return {"received": True, "duplicate": False, "eventId": x_khadakx_event_id}


@router.get("/events")
async def list_received_events(businessId: str = None, db: Session = Depends(get_db)):
    query = db.query(KhadakxEvent)
    if businessId:
        query = query.filter(KhadakxEvent.business_id == businessId)
    events = query.order_by(KhadakxEvent.received_at.desc()).limit(100).all()
    return {
        "count": len(events),
        "events": [
            {
                "eventId": e.event_id,
                "eventType": e.event_type,
                "businessId": e.business_id,
                "contractVersion": e.contract_version,
                "receivedAt": e.received_at.isoformat(),
            }
            for e in events
        ],
    }
