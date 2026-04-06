import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqSummarizer:
    def __init__(self):
        # Connects to Groq using the key in your .env
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.name = "Llama-3.1-Groq"

    def summarize(self, article_title, article_text):
        print(f"⚡ {self.name} is summarizing: {article_title[:50]}...")
        
        prompt = f"""
        You are a tech news expert. Summarize the following TechCrunch article.
        Title: {article_title}
        Content: {article_text[:5000]}
        
        Provide a 3-sentence summary that highlights:
        1. What happened?
        2. Who is involved?
        3. Why does it matter for the tech industry?
        """

        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        # SRE Observability: Capture usage data from the response object
        usage = {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens
        }
        
        # FIXED: Correct way to access content in the Groq SDK
        return completion.choices[0].message.content, usage
