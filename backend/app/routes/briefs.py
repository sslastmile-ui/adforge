from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import Brief, CreativeDNA
from datetime import datetime

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

@router.get("/")
async def get_all_briefs(
    db: Session = Depends(get_db),
    tenant_id: Optional[str] = Query(None)
):
    query = db.query(Brief)
    if tenant_id:
        query = query.filter(Brief.tenant_id == tenant_id)
    briefs = query.order_by(desc(Brief.created_at)).all()
    
    result = []
    for brief in briefs:
        dna = db.query(CreativeDNA).filter(CreativeDNA.brief_id == brief.id).first()
        brief_data = {
            "id": str(brief.id),
            "product_name": brief.product_name,
            "product_description": brief.product_description,
            "offer": brief.offer,
            "target_audience": brief.target_audience,
            "brand_voice": brief.brand_voice,
            "status": brief.status,
            "created_at": brief.created_at.isoformat() if brief.created_at else None,
            "dna": {
                "hook": dna.hook if dna else None,
                "value_prop": dna.value_prop if dna else None,
                "cta": dna.cta if dna else None,
                "visual_sentiment": dna.visual_sentiment if dna else None,
                "status": dna.status if dna else None
            } if dna else None
        }
        result.append(brief_data)
    
    return {"briefs": result, "total": len(result)}

@router.get("/{brief_id}")
async def get_brief(brief_id: str, db: Session = Depends(get_db)):
    brief = db.query(Brief).filter(Brief.id == brief_id).first()
    if not brief:
        raise HTTPException(404, "Brief not found")
    
    dna = db.query(CreativeDNA).filter(CreativeDNA.brief_id == brief_id).first()
    return {
        "id": str(brief.id),
        "product_name": brief.product_name,
        "product_description": brief.product_description,
        "offer": brief.offer,
        "target_audience": brief.target_audience,
        "brand_voice": brief.brand_voice,
        "status": brief.status,
        "created_at": brief.created_at.isoformat() if brief.created_at else None,
        "dna": {
            "hook": dna.hook if dna else None,
            "value_prop": dna.value_prop if dna else None,
            "cta": dna.cta if dna else None,
            "visual_sentiment": dna.visual_sentiment if dna else None,
            "status": dna.status if dna else None
        } if dna else None
    }