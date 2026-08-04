from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from ..database import get_db
from ..models import Brief, CreativeDNA, ChannelAsset
from ..services.ai_service import AIService  # <-- NEW: Import our AI service
import os
import json
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    brief_id: str
    tenant_id: str
    channels: List[str] = ["instagram", "facebook"]

class GenerateResponse(BaseModel):
    dna_id: str
    hook: str
    value_prop: str
    cta: str
    status: str

@router.post("/", response_model=GenerateResponse)
async def generate_creative(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Get the brief
    brief = db.query(Brief).filter(Brief.id == request.brief_id).first()
    if not brief:
        raise HTTPException(404, "Brief not found")
    
    try:
        # ============================================
        # NEW: Use OpenRouter instead of OpenAI
        # ============================================
        ai_service = AIService()
        dna_data = ai_service.generate_creative_dna(
            product_name=brief.product_name,
            offer=brief.offer,
            target_audience=brief.target_audience,
            brand_voice=brief.brand_voice.get("tone", "") if brief.brand_voice else ""
        )
        
        # Save DNA
        dna = CreativeDNA(
            brief_id=request.brief_id,
            tenant_id=request.tenant_id,
            hook=dna_data.get("hook", ""),
            value_prop=dna_data.get("value_prop", ""),
            cta=dna_data.get("cta", ""),
            visual_sentiment=dna_data.get("visual_sentiment", ""),
            status="pending"
        )
        db.add(dna)
        db.commit()
        db.refresh(dna)
        
        # Generate channel assets in background
        background_tasks.add_task(
            generate_channel_assets,
            dna.id,
            request.tenant_id,
            request.channels,
            dna_data
        )
        
        return GenerateResponse(
            dna_id=str(dna.id),
            hook=dna.hook,
            value_prop=dna.value_prop,
            cta=dna.cta,
            status="processing"
        )
        
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        raise HTTPException(500, f"AI generation failed: {str(e)}")

def generate_channel_assets(dna_id, tenant_id, channels, dna_data):
    # This is a background task
    # For now, just log it
    print(f"Generating assets for DNA {dna_id} on channels: {channels}")