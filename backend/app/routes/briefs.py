from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional, List
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

class BriefResponse(BaseModel):
    id: str
    product_name: str
    product_description: Optional[str]
    offer: str
    target_audience: str
    brand_voice: Optional[dict]
    status: str
    created_at: datetime

@router.post("/")
async def create_brief(request: CreateBriefRequest, db: Session = Depends(get_db)):
    """Create a new brief"""
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

@router.get("/")
async def get_all_briefs(
    db: Session = Depends(get_db),
    tenant_id: Optional[str] = Query(None, description="Filter by tenant ID")
):
    """Get all briefs, optionally filtered by tenant"""
    query = db.query(Brief)
    if tenant_id:
        query = query.filter(Brief.tenant_id == tenant_id)
    briefs = query.order_by(desc(Brief.created_at)).all()
    
    return {
        "briefs": [
            {
                "id": str(b.id),
                "product_name": b.product_name,
                "product_description": b.product_description,
                "offer": b.offer,
                "target_audience": b.target_audience,
                "brand_voice": b.brand_voice,
                "status": b.status,
                "created_at": b.created_at.isoformat() if b.created_at else None
            }
            for b in briefs
        ],
        "total": len(briefs)
    }

@router.get("/{brief_id}")
async def get_brief(brief_id: str, db: Session = Depends(get_db)):
    """Get a single brief by ID"""
    brief = db.query(Brief).filter(Brief.id == brief_id).first()
    if not brief:
        raise HTTPException(404, "Brief not found")
    return {
        "id": str(brief.id),
        "product_name": brief.product_name,
        "product_description": brief.product_description,
        "offer": brief.offer,
        "target_audience": brief.target_audience,
        "brand_voice": brief.brand_voice,
        "status": brief.status,
        "created_at": brief.created_at.isoformat() if brief.created_at else None
    }