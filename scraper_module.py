import asyncio
import os
from crawl4ai import AsyncWebCrawler
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def get_top_5_links():
    print("🚀 Extracting homepage with Groq intelligence...")
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://techcrunch.com/", bypass_cache=True)
        
        if not result.success:
            return []

        # Use Groq to find the links
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Find the TOP 5 latest news article URLs from this text. Return ONLY a Python list of strings. \n\n {result.markdown[:8000]}"
            }],
            model="llama-3.1-8b-instant",
        )
        
        try:
            links_text = chat_completion.choices[0].message.content
            # Clean up potential markdown formatting from AI
            clean_list = links_text.replace("```python", "").replace("```", "").strip()
            import ast
            return ast.literal_eval(clean_list)[:5]
        except Exception as e:
            print(f"❌ Groq Link Extraction Failed: {e}")
            return []

if __name__ == "__main__":
    links = asyncio.run(get_top_5_links())
    print(f"Links found: {links}")
