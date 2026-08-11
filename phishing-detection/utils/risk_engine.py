import re
from urllib.parse import urlparse
from datetime import datetime

from utils.feature_extractor import extract_features

def get_domain(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        return urlparse(url).netloc.lower()
    except:
        return ""


def hybrid_risk_score(url, model):

    features = extract_features(url)

    ml_prob = model.predict_proba([features])[0][1] * 100

    domain = get_domain(url)

    ip_flag = 1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}', domain) else 0

    keyword_pressure = features[-1]

    suspicious_signal = ip_flag + keyword_pressure

    # WHOIS skipped here for stability (can be added later safely)

    risk_score = (
        0.6 * ml_prob +
        25 * ip_flag +
        10 * keyword_pressure
    )

    risk_score = min(100, max(0, risk_score))

    return {
        "url": url,
        "risk_score": round(risk_score, 2),
        "ml_probability": round(ml_prob, 2),
        "ip_flag": ip_flag,
        "keyword_score": keyword_pressure,
        "final_label": "PHISHING" if risk_score > 50 else "SAFE"
    }