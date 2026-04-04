import os
from src.scraper import get_top_5_links
from src.summarizer import GroqSummarizer
from src.reporter import create_pdf, send_email
import httpx

def run_agent():
    # 1. Get Links
    links = get_top_5_links()
    if not links:
        print("No articles found.")
        return

    ai = GroqSummarizer()
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}

    # 2. Fetch and Summarize
    with httpx.Client(timeout=15.0) as client:
        for url in links:
            try:
                print(f"--- Reading: {url[:50]}... ---")
                resp = client.get(url, headers=headers)
                summary = ai.summarize(url, resp.text[:10000]) # Send first 10k chars of HTML
                results.append((url, summary))
            except Exception as e:
                print(f"Error processing {url}: {e}")
    
    # 3. Report
    if results:
        pdf_file = create_pdf(results)
        send_email(pdf_file)
        print("✅ Success: PDF generated and Emailed!")

if __name__ == "__main__":
    run_agent()