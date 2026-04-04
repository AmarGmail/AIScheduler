import httpx
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

def get_top_5_links():
    print("🚀 Fetching TechCrunch via HTTPX (Slim Mode)...")
    # A User-Agent header helps avoid being blocked as a bot
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get("https://techcrunch.com", headers=headers)
            resp.raise_for_status()
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = []
        
        # TechCrunch articles usually have the year in the URL
        for a in soup.find_all('a', href=True):
            url = a['href']
            if "://techcrunch.com" in url and url not in links:
                links.append(url)
                if len(links) >= 5:
                    break
        
        print(f"✅ Found {len(links)} articles.")
        return links
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return []