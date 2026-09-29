from .scoring import calculate_score, classify

def qualify_lead(lead, config=None):
    score, checks = calculate_score(lead, config)
    evidence=[]
    labels={'website':'website present','ecommerce_platform':'e-commerce platform identified','wholesale':'wholesale signal','manufacturer':'manufacturer signal','social_selling':'active social-selling signal','whatsapp_ordering':'WhatsApp ordering signal','pan_india_shipping':'Pan-India shipping signal','parcel_friendly':'parcel-friendly category'}
    evidence=[labels[k] for k,v in checks.items() if v]
    missing=[labels[k] for k,v in checks.items() if not v]
    confidence=min(0.98,0.45+0.06*len(evidence))
    explanation='Supported signals: '+(', '.join(evidence) if evidence else 'none identified')+'. Missing/unknown signals: '+(', '.join(missing) if missing else 'none')+'. No missing facts are inferred.'
    return {'score':score,'classification':classify(score,config),'confidence':round(confidence,2),'explanation':explanation}
