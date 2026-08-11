import re
from urllib.parse import urlparse

keywords = ['login', 'verify', 'update', 'secure', 'bank', 'account', 'password']

trusted_domains = [
    "google.com",
    "linkedin.com",
    "github.com",
    "microsoft.com",
    "facebook.com",
    "instagram.com",
    "whatsapp.com",
    "x.com",
    "twitter.com",
    "amazon.com",
    "apple.com",
    "paypal.com",
    "netflix.com",
    "office.com",
    "adobe.com",
    "dropbox.com",
    "cloudflare.com",
    "stackoverflow.com",
    "reddit.com",
    "yahoo.com",
    "zoom.us",
    "canva.com"
]

suspicious_tlds = [
    ".xyz", ".tk", ".ru", ".top", ".click",
    ".online", ".site", ".website", ".space",
    ".icu", ".live", ".support", ".download",
    ".shop", ".fun"
]

def get_domain(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain
    except:
        return ""

def extract_features(url):
    features = []

    domain = get_domain(url)

    # 1. URL length
    features.append(len(url))

    # 2. dot count
    features.append(url.count('.'))

    # 3. slash count
    features.append(url.count('/'))

    # 4. hyphen count
    features.append(url.count('-'))

    # 5. @ symbol
    features.append(1 if '@' in url else 0)

    # 6. HTTPS
    features.append(1 if url.startswith("https://") else 0)

    # 7. HTTP
    features.append(1 if url.startswith("http://") else 0)

    # 8. no protocol
    features.append(1 if not url.startswith(("http://", "https://")) else 0)

    # 9. IP address detection
    ip_pattern = r'\d+\.\d+\.\d+\.\d+'
    features.append(1 if re.search(ip_pattern, url) else 0)

    # 10. trusted domain (SAFE MATCH)
    features.append(1 if domain in trusted_domains else 0)

    # 11. subdomain depth
    features.append(domain.count('.') - 1 if domain else 0)

    # 12. suspicious TLD
    features.append(1 if any(tld in domain for tld in suspicious_tlds) else 0)

    # 13. keyword score
    features.append(sum(1 for k in keywords if k in url.lower()))

    return features