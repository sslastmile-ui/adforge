from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import Brief, Tenant
from datetime import datetime
import uuid

router = APIRouter()

class CreateBriefRequest(BaseModel):
    tenant_id: str
    product_name: str
    product_description: Optional[str] = None
    offer: str
    target_audience: str
    brand_voice: Optional[dict] = {}

@router.post("/")
async def create_brief(request: CreateBriefRequest, db: Session = Depends(get_db)):
    brief = Brief(
        tenant_id=request.tenant_id,
        product_name=request.product_name,
        product_description=request.product_description,
        offer=request.offer,
        target_audience=request.target_audience,
        brand_voice=request.brand_voice
    )
    db.add(brief)
    db.commit()
    db.refresh(brief)
    return {"id": str(brief.id), "status": brief.status}

@router.get("/{brief_id}")
async def get_brief(brief_id: str, db: Session = Depends(get_db)):
    brief = db.query(Brief).filter(Brief.id == brief_id).first()
    if not brief:
        raise HTTPException(404, "Brief not found")
    return {
        "id": str(brief.id),
        "product_name": brief.product_name,
        "offer": brief.offer,
        "target_audience": brief.target_audience,
        "status": brief.status
    }