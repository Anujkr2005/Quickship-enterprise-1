from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from .database import Base, engine, get_db
from .models import Lead, ScoreConfig, Campaign
from .schemas import LeadCreate, LeadOut, LeadUpdate, ScoreConfigIn, CampaignIn, CampaignOut, CampaignUpdate
from .ai import qualify_lead

Base.metadata.create_all(bind=engine)
app=FastAPI(title='Quickship AI Lead Generation & Sales CRM',version='2.0.0',description='MVP/production-ready foundation for compliant lead discovery, qualification, scoring and CRM operations.')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

def config(db):
    c=db.query(ScoreConfig).first()
    if not c: c=ScoreConfig(); db.add(c); db.commit(); db.refresh(c)
    return c

def apply_ai(lead,db):
    ai=qualify_lead(lead,config(db)); lead.score=ai['score']; lead.classification=ai['classification']; lead.confidence=ai['confidence']; lead.ai_explanation=ai['explanation']

@app.get('/api/health')
def health(): return {'ok':True,'service':'quickship-crm','version':'2.0.0'}

@app.post('/api/leads',response_model=LeadOut)
def create_lead(payload:LeadCreate,db:Session=Depends(get_db)):
    name=payload.business_name.strip().lower(); existing=db.query(Lead).filter(func.lower(Lead.business_name)==name).first()
    if payload.website:
        existing=existing or db.query(Lead).filter(Lead.website==payload.website).first()
    if existing: raise HTTPException(409,'Possible duplicate lead already exists')
    lead=Lead(**payload.model_dump()); apply_ai(lead,db); db.add(lead); db.commit(); db.refresh(lead); return lead

@app.get('/api/leads',response_model=list[LeadOut])
def list_leads(search:str='',status:str='',classification:str='',source:str='',db:Session=Depends(get_db)):
    q=db.query(Lead)
    if search:
        like=f'%{search}%'; q=q.filter(or_(Lead.business_name.ilike(like),Lead.city.ilike(like),Lead.category.ilike(like),Lead.public_contact.ilike(like)))
    if status:q=q.filter(Lead.status==status)
    if classification:q=q.filter(Lead.classification==classification)
    if source:q=q.filter(Lead.source==source)
    return q.order_by(Lead.score.desc(),Lead.created_at.desc()).all()

@app.patch('/api/leads/{lead_id}',response_model=LeadOut)
def update_lead(lead_id:int,payload:LeadUpdate,db:Session=Depends(get_db)):
    lead=db.get(Lead,lead_id)
    if not lead:raise HTTPException(404,'Lead not found')
    for k,v in payload.model_dump(exclude_none=True).items():setattr(lead,k,v)
    db.commit();db.refresh(lead);return lead

@app.post('/api/leads/{lead_id}/qualify',response_model=LeadOut)
def requalify(lead_id:int,db:Session=Depends(get_db)):
    lead=db.get(Lead,lead_id)
    if not lead:raise HTTPException(404,'Lead not found')
    apply_ai(lead,db);db.commit();db.refresh(lead);return lead

@app.get('/api/dashboard')
def dashboard(db:Session=Depends(get_db)):
    leads=db.query(Lead).all()
    return {'total':len(leads),'hot':sum(x.classification=='HOT' for x in leads),'warm':sum(x.classification=='WARM' for x in leads),'normal':sum(x.classification=='NORMAL' for x in leads),'low':sum(x.classification=='LOW' for x in leads),'new':sum(x.status=='New' for x in leads),'contacted':sum(x.status=='Contacted' for x in leads),'interested':sum(x.status=='Interested' for x in leads),'qualified':sum(x.status=='Qualified' for x in leads),'quotations':sum(x.status=='Quotation Sent' for x in leads),'converted':sum(x.status=='Converted' for x in leads)}

@app.get('/api/config/scoring')
def get_scoring(db:Session=Depends(get_db)):
    return {k:getattr(config(db),k) for k in ['website','ecommerce_platform','wholesale','manufacturer','social_selling','whatsapp_ordering','pan_india_shipping','parcel_friendly','hot_min','warm_min','normal_min']}

@app.put('/api/config/scoring')
def set_scoring(payload:ScoreConfigIn,db:Session=Depends(get_db)):
    c=config(db)
    for k,v in payload.model_dump().items():setattr(c,k,v)
    db.commit();return {'saved':True}

@app.get('/api/campaigns',response_model=list[CampaignOut])
def campaigns(db:Session=Depends(get_db)): return db.query(Campaign).order_by(Campaign.id.desc()).all()
@app.post('/api/campaigns',response_model=CampaignOut)
def create_campaign(payload:CampaignIn,db:Session=Depends(get_db)):
    c=Campaign(**payload.model_dump());db.add(c);db.commit();db.refresh(c);return c

@app.patch('/api/campaigns/{campaign_id}',response_model=CampaignOut)
def update_campaign(campaign_id:int,payload:CampaignUpdate,db:Session=Depends(get_db)):
    c=db.get(Campaign,campaign_id)
    if not c:raise HTTPException(404,'Campaign not found')
    for k,v in payload.model_dump(exclude_none=True).items():setattr(c,k,v)
    db.commit();db.refresh(c);return c