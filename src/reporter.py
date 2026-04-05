import os
import yagmail
from datetime import datetime
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import httpx

load_dotenv()

def create_pdf(summaries, filename="daily_news.pdf"):
    """Generates a professional-grade PDF report."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom SRE-style headers
    title_style = styles['Heading1']
    link_style = ParagraphStyle('link', parent=styles['Normal'], textColor=colors.blue, fontSize=8)
    summary_style = styles['Normal']
    
    elements = []
    elements.append(Paragraph(f"<b>Tech Briefing</b>: {datetime.now().strftime('%d %B %Y')}", title_style))
    elements.append(Spacer(1, 12))

    for url, summary in summaries:
        elements.append(Paragraph(f"<b>SOURCE:</b> {url}", link_style))
        elements.append(Spacer(1, 8))
        
        # Cleaning AI markers if any (like **)
        clean_summary = summary.replace('**', '').replace('\n', '<br/>')
        elements.append(Paragraph(clean_summary, summary_style))
        
        elements.append(Spacer(1, 15))
        elements.append(Paragraph("<hr width='100%' color='lightgrey'/>", styles['Normal']))
        elements.append(Spacer(1, 10))

    doc.build(elements)
    return filename

def send_email(pdf_path):
    """Sends the PDF via Gmail using App Passwords."""
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    if not user or not password:
        print("❌ Email credentials missing in .env")
        return

    yag = yagmail.SMTP(user, password)
    subject = f"Daily Tech Report - {datetime.now().strftime('%Y-%m-%d')}"
    body = "Hello,\n\nAttached is your automated AI News Summary for today.\n\nBest,\nYour AI Agent"
    
    yag.send(to=user, subject=subject, contents=body, attachments=pdf_path)


def send_heartbeat():
    url = os.getenv("HEALTHCHECK_URL")
    if url:
        try:
            httpx.get(url, timeout=5.0)
            print("💓 Healthcheck heartbeat sent!")
        except Exception as e:
            print(f"⚠️ Heartbeat failed: {e}")
