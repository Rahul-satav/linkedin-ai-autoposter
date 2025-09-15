# daily_linkedin_ai_news.py
# Fetch top AI news (NewsAPI or RSS) and post to LinkedIn UGC API
# Needs environment variables: LINKEDIN_ACCESS_TOKEN, NEWSAPI_KEY, PROFILE_URN (optional)

import os, requests
from datetime import datetime
from urllib.parse import urlparse

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
PROFILE_URN = os.getenv("PROFILE_URN")  # optional: urn:li:person:xxxxx or just id

HEADERS = {
    "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json"
}

def get_member_id():
    if not LINKEDIN_ACCESS_TOKEN:
        raise Exception("LINKEDIN_ACCESS_TOKEN not set")
    if PROFILE_URN:
        if PROFILE_URN.startswith("urn:li:person:"):
            return PROFILE_URN.split(":")[-1]
        return PROFILE_URN
    url = "https://api.linkedin.com/v2/me"
    r = requests.get(url, headers={"Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}"}, timeout=15)
    r.raise_for_status()
    return r.json().get("id")

def fetch_top_ai_article_newsapi():
    if not NEWSAPI_KEY:
        return None
    params = {
        "q": "artificial intelligence OR AI OR machine learning",
        "language": "en",
        "pageSize": 5,
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY
    }
    r = requests.get("https://newsapi.org/v2/everything", params=params, timeout=15)
    r.raise_for_status()
    articles = r.json().get("articles", [])
    return articles[0] if articles else None

def fetch_top_ai_article_rss():
    # fallback using RSS feeds if no NewsAPI key
    feeds = [
        "https://www.technologyreview.com/feed/",
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.feedburner.com/TechCrunch/"
    ]
    for feed in feeds:
        try:
            r = requests.get(feed, timeout=10)
            if r.status_code != 200:
                continue
            text = r.text
            if "<item" in text:
                try:
                    title = text.split("<title>")[1].split("</title>")[0]
                    link = text.split("<link>")[1].split("</link>")[0]
                    desc = ""
                    if "<description>" in text:
                        desc = text.split("<description>")[1].split("</description>")[0]
                    return {
                        "title": title,
                        "description": desc,
                        "url": link,
                        "source": {"name": urlparse(feed).netloc},
                        "publishedAt": ""
                    }
                except Exception:
                    continue
        except Exception:
            continue
    return None

def craft_post_text(article):
    title = (article.get("title") or "").strip()
    desc = (article.get("description") or "").strip()
    src = article.get("source", {}).get("name", "")
    url = article.get("url", "")
    date = (article.get("publishedAt") or "")[:10]
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    hashtags = "#AI #MachineLearning #ArtificialIntelligence"
    text = f"{title}\n\n{desc}\n\nSource: {src} • {date}\n{url}\n\n{hashtags}"
    return text[:2800]

def post_to_linkedin(text, member_id):
    author = f"urn:li:person:{member_id}"
    body = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"}
    }
    url = "https://api.linkedin.com/v2/ugcPosts"
    r = requests.post(url, headers=HEADERS, json=body, timeout=15)
    if r.status_code not in (201, 200):
        raise Exception(f"LinkedIn API error: {r.status_code} - {r.text}")
    return r.json()

def main():
    try:
        member_id = get_member_id()
        article = fetch_top_ai_article_newsapi()
        if not article:
            article = fetch_top_ai_article_rss()
        if not article:
            print("[INFO] No article found.")
            return
        text = craft_post_text(article)
        resp = post_to_linkedin(text, member_id)
        print("[SUCCESS] Posted:", resp.get("id", "unknown"))
    except Exception as e:
        print("[ERROR]", str(e))

if __name__ == "__main__":
    main()
