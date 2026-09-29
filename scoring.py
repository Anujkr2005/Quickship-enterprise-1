WEIGHTS = {'website':20,'ecommerce_platform':15,'wholesale':15,'manufacturer':10,'social_selling':10,'whatsapp_ordering':10,'pan_india_shipping':10,'parcel_friendly':10}

def _weight(config, key):
    if config is None:
        return WEIGHTS[key]
    if isinstance(config, dict):
        return config[key]
    return getattr(config, key)  # database ScoreConfig object

def calculate_score(lead, config=None):
    checks={
      'website': bool((lead.website or '').strip()),
      'ecommerce_platform': (lead.ecommerce_platform or 'Unknown') != 'Unknown',
      'wholesale': bool(lead.wholesale),'manufacturer':bool(lead.manufacturer),
      'social_selling':bool(lead.social_selling),'whatsapp_ordering':bool(lead.whatsapp_ordering),
      'pan_india_shipping':bool(lead.pan_india_shipping),'parcel_friendly':bool(lead.parcel_friendly)}
    return min(100,sum(_weight(config,k) for k,v in checks.items() if v)),checks

def classify(score, config=None):
    hot,warm,normal=(80,60,40) if not config else (config.hot_min,config.warm_min,config.normal_min)
    if score>=hot:return 'HOT'
    if score>=warm:return 'WARM'
    if score>=normal:return 'NORMAL'
    return 'LOW'

# WEIGHTS = {'website':20,'ecommerce_platform':15,'wholesale':15,'manufacturer':10,'social_selling':10,'whatsapp_ordering':10,'pan_india_shipping':10,'parcel_friendly':10}

# def calculate_score(lead, config=None):
#     w = config or WEIGHTS
#     checks={
#       'website': bool((lead.website or '').strip()),
#       'ecommerce_platform': (lead.ecommerce_platform or 'Unknown') != 'Unknown',
#       'wholesale': bool(lead.wholesale),'manufacturer':bool(lead.manufacturer),
#       'social_selling':bool(lead.social_selling),'whatsapp_ordering':bool(lead.whatsapp_ordering),
#       'pan_india_shipping':bool(lead.pan_india_shipping),'parcel_friendly':bool(lead.parcel_friendly)}
#     return min(100,sum(w[k] for k,v in checks.items() if v)),checks

# def classify(score, config=None):
#     hot,warm,normal=(80,60,40) if not config else (config.hot_min,config.warm_min,config.normal_min)
#     if score>=hot:return 'HOT'
#     if score>=warm:return 'WARM'
#     if score>=normal:return 'NORMAL'
#     return 'LOW'
