import httpx
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

def get_top_5_links():
    print("🚀 Fetching TechCrunch Headlines...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            resp = client.get("https://techcrunch.com", headers=headers)
            resp.raise_for_status()
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = []
        # Target main article links (usually in h2 or h3 tags on TC)
        for a in soup.find_all('a', href=True):
            url = a['href']
            # Ensure it's a direct article link and not a category/author page
            # if "://techcrunch.com" in url and url not in links:
            if "techcrunch.com/20" in url and url not in links:
                links.append(url)
                if len(links) >= 5: break
        return links
    except Exception as e:
        print(f"❌ Scraper Error: {e}")
        return []

def extract_article_text(url):
    """New helper to get ONLY the article body text"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Remove scripts, styles, and ads
            for script in soup(["script", "style", "aside", "header", "footer", "nav"]):
                script.decompose()
            
            # TechCrunch articles usually live in <p> tags within the entry-content div
            paragraphs = soup.find_all('p')
            article_text = "\n".join([p.get_text() for p in paragraphs])
            return article_text[:6000] # Limit to 6000 chars for LLM efficiency
    except:
        return "Could not extract content."