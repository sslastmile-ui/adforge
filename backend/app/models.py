from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True, nullable=False)
    plan = Column(String, default="free")
    created_at = Column(DateTime, default=datetime.utcnow)

class Brief(Base):
    __tablename__ = "briefs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    product_name = Column(String, nullable=False)
    product_description = Column(Text, nullable=True)
    offer = Column(String, nullable=False)
    target_audience = Column(String, nullable=False)
    brand_voice = Column(JSON, default={})
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)

class CreativeDNA(Base):
    __tablename__ = "creative_dnas"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    brief_id = Column(String, ForeignKey("briefs.id"), nullable=False)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    hook = Column(Text, nullable=False)
    value_prop = Column(Text, nullable=False)
    cta = Column(String, nullable=False)
    visual_sentiment = Column(Text, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class ChannelAsset(Base):
    __tablename__ = "channel_assets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dna_id = Column(String, ForeignKey("creative_dnas.id"), nullable=False)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    channel = Column(String, nullable=False)
    spec = Column(JSON, nullable=False)
    status = Column(String, default="draft")
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)