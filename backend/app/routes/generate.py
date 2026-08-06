from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from ..database import get_db
from ..models import Brief, CreativeDNA, ChannelAsset
from ..services.ai_service import AIService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    brief_id: str
    tenant_id: str
    channels: List[str] = ["instagram", "facebook"]

@router.post("/")
async def generate_creative(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    brief = db.query(Brief).filter(Brief.id == request.brief_id).first()
    if not brief:
        raise HTTPException(404, "Brief not found")
    
    try:
        ai_service = AIService()
        dna_data = ai_service.generate_creative_dna(
            product_name=brief.product_name,
            offer=brief.offer,
            target_audience=brief.target_audience,
            brand_voice=brief.brand_voice.get("tone", "") if brief.brand_voice else ""
        )
        
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
        
        background_tasks.add_task(
            generate_channel_assets,
            dna.id,
            request.tenant_id,
            request.channels,
            dna_data
        )
        
        return {"dna_id": str(dna.id), "hook": dna.hook, "value_prop": dna.value_prop, "cta": dna.cta, "status": "processing"}
        
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        raise HTTPException(500, f"AI generation failed: {str(e)}")

def generate_channel_assets(dna_id, tenant_id, channels, dna_data):
    from ..database import SessionLocal
    db = SessionLocal()
    
    try:
        dna = db.get(CreativeDNA, dna_id)
        if not dna:
            return
        
        channel_specs = {
            "instagram": {"caption": f"{dna.hook}\n\n{dna.value_prop}\n\n{dna.cta}", "hashtags": "#D2C #Sale", "image_prompt": dna.visual_sentiment},
            "facebook": {"primary_text": f"{dna.hook}\n\n{dna.value_prop}", "headline": dna.hook, "call_to_action": dna.cta},
            "google": {"headlines": [dna.hook[:30], dna.value_prop[:30]], "descriptions": [dna.value_prop[:90]]},
            "linkedin": {"title": dna.hook, "content": f"{dna.hook}\n\n{dna.value_prop}"},
            "pinterest": {"title": dna.hook, "description": dna.value_prop}
        }
        
        for channel, specs in channel_specs.items():
            if channel in channels:
                asset = ChannelAsset(dna_id=dna_id, tenant_id=tenant_id, channel=channel, spec=specs, status="draft")
                db.add(asset)
        
        dna.status = "approved"
        db.commit()
    except Exception as e:
        logger.error(f"Channel asset generation failed: {e}")
        db.rollback()
    finally:
        db.close()