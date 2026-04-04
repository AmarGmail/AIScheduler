import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import yagmail
from datetime import datetime

def create_pdf(summaries, filename="daily_news.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"AI News Report - {datetime.now().strftime('%Y-%m-%d')}")
    y = 700
    for title, summary in summaries:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(100, y, f"Link: {title[:70]}...")
        y -= 20
        c.setFont("Helvetica", 9)
        text = c.beginText(100, y)
        text.textLines(summary)
        c.drawText(text)
        y -= 60
    c.save()
    return filename

def send_email(pdf_path):
    yag = yagmail.SMTP(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
    yag.send(to=os.getenv("EMAIL_USER"), 
             subject=f"Daily AI Report {datetime.now().date()}", 
             attachments=pdf_path)
