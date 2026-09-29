from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Float
from sqlalchemy.sql import func
from .database import Base

class Lead(Base):
    __tablename__='leads'
    id=Column(Integer,primary_key=True,index=True)
    business_name=Column(String(200),nullable=False,index=True)
    category=Column(String(120),default='Unknown')
    subcategory=Column(String(120),default='Unknown')
    city=Column(String(120),default='Unknown',index=True)
    area=Column(String(120),default='Unknown')
    website=Column(String(500),default='')
    source=Column(String(120),default='Manual',index=True)
    source_url=Column(String(1000),default='')
    public_contact=Column(String(200),default='')
    social_links=Column(Text,default='')
    ecommerce_platform=Column(String(80),default='Unknown')
    business_type=Column(String(80),default='Unknown')
    online_selling=Column(Boolean,default=False)
    wholesale=Column(Boolean,default=False)
    manufacturer=Column(Boolean,default=False)
    social_selling=Column(Boolean,default=False)
    whatsapp_ordering=Column(Boolean,default=False)
    pan_india_shipping=Column(Boolean,default=False)
    parcel_friendly=Column(Boolean,default=False)
    shipping_signals=Column(Text,default='')
    score=Column(Integer,default=0,index=True)
    classification=Column(String(20),default='LOW',index=True)
    confidence=Column(Float,default=0.0)
    ai_explanation=Column(Text,default='')
    salesperson=Column(String(120),default='Unassigned')
    status=Column(String(40),default='New',index=True)
    notes=Column(Text,default='')
    next_follow_up=Column(String(40),default='')
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

class ScoreConfig(Base):
    __tablename__='score_config'
    id=Column(Integer,primary_key=True)
    website=Column(Integer,default=20); ecommerce_platform=Column(Integer,default=15)
    wholesale=Column(Integer,default=15); manufacturer=Column(Integer,default=10)
    social_selling=Column(Integer,default=10); whatsapp_ordering=Column(Integer,default=10)
    pan_india_shipping=Column(Integer,default=10); parcel_friendly=Column(Integer,default=10)
    hot_min=Column(Integer,default=80); warm_min=Column(Integer,default=60); normal_min=Column(Integer,default=40)

class Campaign(Base):
    __tablename__='campaigns'
    id=Column(Integer,primary_key=True)
    name=Column(String(200),nullable=False)
    city_area=Column(String(200),default='Pan India')
    category=Column(String(120),default='All')
    sources=Column(String(500),default='')
    target_volume=Column(Integer,default=100)
    status=Column(String(30),default='Draft')
    created_at=Column(DateTime(timezone=True),server_default=func.now())
