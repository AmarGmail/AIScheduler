import os
import sys
from dotenv import load_dotenv

# Import our modular logic from the src directory
from src.scraper import get_top_5_links, extract_article_text
from src.summarizer import GroqSummarizer
from src.reporter import create_pdf, send_email, send_heartbeat

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
    
    # Initialize observability metrics
    total_metrics = {"prompt": 0, "completion": 0, "total": 0}

    # 3. Process each article
    for url in links:
        print(f"\n--- Processing: {url[:60]}... ---")
        
        # Extract clean text
        content = extract_article_text(url)
        
        # SRE Check: Ensure content is substantial enough to summarize
        if len(content) > 300:
            try:
                # We now expect the summarizer to return (text, usage_dict)
                summary, usage = ai.summarize(url, content)
                results.append((url, summary))
                
                # Accumulate tokens for the final report
                total_metrics["prompt"] += usage.get("prompt_tokens", 0)
                total_metrics["completion"] += usage.get("completion_tokens", 0)
                total_metrics["total"] += usage.get("total_tokens", 0)
                
            except Exception as e:
                print(f"❌ AI Error processing {url}: {e}")
        else:
            print(f"⚠️ Content too short or blocked for {url}. Skipping.")

    # 4. Generate Professional PDF, Email it, and Ping Healthcheck
    if results:
        print(f"\n📄 Generating PDF with Usage Metrics...")
        try:
            # Create PDF including the metrics footer
            pdf_path = create_pdf(results, filename="daily_news.pdf", metrics=total_metrics)
            
            print(f"📧 Sending report to {os.getenv('EMAIL_USER')}...")
            send_email(pdf_path)
            
            # SRE Observability: Ping the heartbeat only after full success
            send_heartbeat()
            
            print("✅ Mission Success: Report delivered and Heartbeat sent.")
        except Exception as e:
            print(f"❌ Reporting/Monitoring Error: {e}")
    else:
        print("❌ No valid summaries were generated. No email sent.")

if __name__ == "__main__":
    try:
        run_agent()
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped by user.")
        sys.exit(0)
