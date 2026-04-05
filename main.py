import os
import sys
from dotenv import load_dotenv

# Import our modular logic from the src directory
from src.scraper import get_top_5_links, extract_article_text
from src.summarizer import GroqSummarizer
from src.reporter import create_pdf, send_email

# Load environment variables
load_dotenv()

def run_agent():
    print("🤖 AI News Agent starting...")

    # 1. Fetch the latest headlines
    links = get_top_5_links()
    if not links:
        print("⚠️ No articles found on TechCrunch. Exiting.")
        return

    # 2. Initialize the AI Summarizer (Groq Llama-3.1)
    ai = GroqSummarizer()
    results = []

    # 3. Process each article
    for url in links:
        print(f"\n--- Processing: {url[:60]}... ---")
        
        # Extract clean text instead of raw HTML
        content = extract_article_text(url)
        
        # SRE Check: Ensure content is substantial enough to summarize
        if len(content) > 300:
            try:
                summary = ai.summarize(url, content)
                results.append((url, summary))
            except Exception as e:
                print(f"❌ AI Error processing {url}: {e}")
        else:
            print(f"⚠️ Content too short or blocked for {url}. Skipping.")

    # 4. Generate Professional PDF and Email it
    if results:
        print(f"\n📄 Generating PDF for {len(results)} articles...")
        try:
            pdf_path = create_pdf(results)
            print(f"📧 Sending report to {os.getenv('EMAIL_USER')}...")
            send_email(pdf_path)
            print("✅ Mission Success: Report delivered to inbox.")
        except Exception as e:
            print(f"❌ Reporting Error: {e}")
    else:
        print("❌ No valid summaries were generated. No email sent.")

if __name__ == "__main__":
    try:
        run_agent()
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user.")
        sys.exit(0)
