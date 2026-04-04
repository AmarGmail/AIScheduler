import asyncio
from scraper_module import get_top_5_links
from ai_module import GroqSummarizer
from crawl4ai import AsyncWebCrawler

async def run_agent():
    # 1. Get the URLs
    links = await get_top_5_links()
    if not links:
        print("No links found. Exiting.")
        return

    # 2. Initialize the AI
    # ai = GeminiSummarizer()
    ai = GroqSummarizer()

    
    # 3. Scrape and Summarize each article
    async with AsyncWebCrawler() as crawler:
        for url in links:
            print(f"\n--- Processing: {url} ---")
            
            # Scrape the full article content
            result = await crawler.arun(url=url)
            
            if result.success:
                # Get summary from AI
                summary = ai.summarize(url, result.markdown)
                print(f"\nSUMMARY:\n{summary}")
            else:
                print(f"Failed to read article at {url}")

if __name__ == "__main__":
    asyncio.run(run_agent())
