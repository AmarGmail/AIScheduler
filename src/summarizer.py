import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqSummarizer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.name = "Llama-3.1-Groq"

    def summarize(self, article_title, article_text):
        print(f"⚡ {self.name} is summarizing: {article_title[:50]}...")
        prompt = f"""
        You are a tech news expert. Summarize this article:
        Title: {article_title}
        Content: {article_text[:5000]}
        
        Provide a 3-sentence summary highlighting What happened, Who is involved, and Why it matters.
        """
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
