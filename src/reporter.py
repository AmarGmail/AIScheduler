import os
import yagmail
import httpx
from datetime import datetime
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

load_dotenv()

def create_pdf(summaries, filename="daily_news.pdf", metrics=None):
    """Generates a professional-grade PDF report with an observability section."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom SRE-style styles
    title_style = styles['Heading1']
    sub_title_style = styles['Heading2']
    link_style = ParagraphStyle('link', parent=styles['Normal'], textColor=colors.blue, fontSize=8)
    summary_style = styles['Normal']
    metrics_style = ParagraphStyle('metrics', parent=styles['Normal'], fontSize=9, leading=12)
    
    elements = []
    
    # Title
    elements.append(Paragraph(f"<b>Tech Briefing</b>: {datetime.now().strftime('%d %B %Y')}", title_style))
    elements.append(Spacer(1, 12))

    # News Articles
    for url, summary in summaries:
        elements.append(Paragraph(f"<b>SOURCE:</b> {url}", link_style))
        elements.append(Spacer(1, 8))
        
        # Cleaning AI markers if any (like **) and converting newlines for PDF
        clean_summary = summary.replace('**', '').replace('\n', '<br/>')
        elements.append(Paragraph(clean_summary, summary_style))
        
        elements.append(Spacer(1, 15))
        elements.append(Paragraph("<hr width='100%' color='lightgrey'/>", styles['Normal']))
        elements.append(Spacer(1, 10))

    # --- NEW: Observability & Usage Section ---
    if metrics:
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("📊 API Usage & Observability", sub_title_style))
        elements.append(Spacer(1, 5))
        
        usage_text = (
            f"<b>Model:</b> Llama-3.1-8b-instant<br/>"
            f"<b>Prompt Tokens:</b> {metrics.get('prompt', 0)}<br/>"
            f"<b>Completion Tokens:</b> {metrics.get('completion', 0)}<br/>"
            f"<b>Total Tokens Consumed:</b> {metrics.get('total', 0)}"
        )
        elements.append(Paragraph(usage_text, metrics_style))

    doc.build(elements)
    return filename

def send_email(pdf_path):
    """Sends the PDF via Gmail using App Passwords."""
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    if not user or not password:
        print("❌ Email credentials missing in .env")
        return

    try:
        yag = yagmail.SMTP(user, password)
        subject = f"Daily Tech Report - {datetime.now().strftime('%Y-%m-%d')}"
        body = "Hello,\n\nAttached is your automated AI News Summary for today.\n\nBest,\nYour AI Agent"
        
        yag.send(to=user, subject=subject, contents=body, attachments=pdf_path)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_heartbeat():
    """Pings the Healthcheck URL to signal job success."""
    url = os.getenv("HEALTHCHECK_URL")
    if url:
        try:
            # We use httpx as it's already in our requirements
            with httpx.Client() as client:
                client.get(url, timeout=10.0)
            print("💓 Healthcheck heartbeat sent!")
        except Exception as e:
            print(f"⚠️ Heartbeat failed: {e}")
