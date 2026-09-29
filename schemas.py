from pydantic import BaseModel, ConfigDict
from typing import Optional

class LeadBase(BaseModel):
    business_name:str; category:str='Unknown'; subcategory:str='Unknown'; city:str='Unknown'; area:str='Unknown'; website:str=''; source:str='Manual'; source_url:str=''; public_contact:str=''; social_links:str=''; ecommerce_platform:str='Unknown'; business_type:str='Unknown'; online_selling:bool=False; wholesale:bool=False; manufacturer:bool=False; social_selling:bool=False; whatsapp_ordering:bool=False; pan_india_shipping:bool=False; parcel_friendly:bool=False; shipping_signals:str=''; salesperson:str='Unassigned'; status:str='New'; notes:str=''; next_follow_up:str=''
class LeadCreate(LeadBase): pass
class LeadUpdate(BaseModel):
    model_config=ConfigDict(extra='forbid')
    status:Optional[str]=None; salesperson:Optional[str]=None; notes:Optional[str]=None; next_follow_up:Optional[str]=None
    category:Optional[str]=None; city:Optional[str]=None; website:Optional[str]=None
class LeadOut(LeadBase):
    model_config=ConfigDict(from_attributes=True)
    id:int; score:int; classification:str; confidence:float; ai_explanation:str
class ScoreConfigIn(BaseModel):
    website:int=20; ecommerce_platform:int=15; wholesale:int=15; manufacturer:int=10; social_selling:int=10; whatsapp_ordering:int=10; pan_india_shipping:int=10; parcel_friendly:int=10; hot_min:int=80; warm_min:int=60; normal_min:int=40
class CampaignIn(BaseModel):
    name:str; city_area:str='Pan India'; category:str='All'; sources:str=''; target_volume:int=100
class CampaignOut(CampaignIn):
    id:int; status:str
    model_config=ConfigDict(from_attributes=True)
class CampaignUpdate(BaseModel):
    model_config=ConfigDict(extra='forbid')
    name:Optional[str]=None; city_area:Optional[str]=None; category:Optional[str]=None
    sources:Optional[str]=None; target_volume:Optional[int]=None; status:Optional[str]=None