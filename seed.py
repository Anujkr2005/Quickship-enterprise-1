from app.database import Base,engine,SessionLocal
from app.models import Lead
from app.ai import qualify_lead
Base.metadata.create_all(bind=engine)
db=SessionLocal()
if not db.query(Lead).count():
    items=[
      Lead(business_name='UrbanKart Store',category='Fashion & Lifestyle',city='Delhi',website='https://example.com',source='Demo Import',ecommerce_platform='Shopify',business_type='D2C',online_selling=True,wholesale=False,social_selling=True,whatsapp_ordering=True,pan_india_shipping=True,parcel_friendly=True,shipping_signals='Pan India delivery, COD available'),
      Lead(business_name='Bharat Home Goods',category='Home & Kitchen',city='Jaipur',source='Demo Import',business_type='Wholesaler',online_selling=True,wholesale=True,manufacturer=False,social_selling=False,whatsapp_ordering=True,pan_india_shipping=True,parcel_friendly=True,shipping_signals='Wholesale orders, courier available')]
    for x in items:
        a=qualify_lead(x);x.score=a['score'];x.classification=a['classification'];x.confidence=a['confidence'];x.ai_explanation=a['explanation'];db.add(x)
    db.commit()
db.close()
print('Seed complete')
