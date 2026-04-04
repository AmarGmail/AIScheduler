import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import yagmail
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def create_pdf(summaries, filename="daily_news.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"TechCrunch Daily Summary - {datetime.now().strftime('%Y-%m-%d')}")
    
    y_position = 720
    c.setFont("Helvetica", 12)
    
    for title, summary in summaries:
        if y_position < 100:  # Start new page if out of space
            c.showPage()
            y_position = 750
            
        c.setFont("Helvetica-Bold", 11)
        c.drawString(100, y_position, f"Source: {title[:80]}...")
        y_position -= 20
        
        c.setFont("Helvetica", 10)
        # Simple text wrapping logic
        text_object = c.beginText(100, y_position)
        text_object.textLines(summary)
        c.drawText(text_object)
        
        y_position -= 60  # Space between articles
        
    c.save()
    return filename

def send_email(pdf_path):
    receiver = os.getenv("EMAIL_USER")
    yag = yagmail.SMTP(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
    yag.send(
        to=receiver,
        subject=f"Daily AI News Report - {datetime.now().strftime('%Y-%m-%d')}",
        contents="Please find your daily tech news summary attached.",
        attachments=pdf_path
    )
    print("✅ Email sent successfully!")
