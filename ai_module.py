import os
from dotenv import load_dotenv
# Load API key from the .env file we created
load_dotenv()

#import google.generativeai as genai
from groq import Groq



# genai.configure(api_key=os.getenv("GROQ_API_KEY"))

# class GeminiSummarizer:
#    def __init__(self):
#        self.model = genai.GenerativeModel('gemini-2.5-flash')
#        self.name = "Gemini-2.5-Flash"

#    def summarize(self, article_title, article_text):
#        print(f"🤖 {self.name} is summarizing: {article_title}...")
        
#        prompt = f"""
#        You are a tech news expert. Summarize the following TechCrunch article.
#        Title: {article_title}
#        Content: {article_text}
        
#        Provide a 3-sentence summary that highlights:
#        1. What happened?
#        2. Who is involved?
#        3. Why does it matter for the tech industry?
#        """
        
#       response = self.model.generate_content(prompt)
#        return response.text



class GroqSummarizer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.name = "Llama-3-Groq"

    def summarize(self, article_title, article_text):
        print(f"⚡ {self.name} is summarizing (FAST)...")
        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Summarize this: {article_text[:5000]}"}]
        )
        return completion.choices[0].message.content

# This part lets us test the module independently
if __name__ == "__main__":
    test_summarizer = GeminiSummarizer()
    sample_text = "SpaceX launched another Starlink mission today from Florida..."
    print(test_summarizer.summarize("SpaceX Launch", sample_text))

