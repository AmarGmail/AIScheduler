import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import yagmail
from datetime import datetime

def create_pdf(summaries, filename="daily_news.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles for a cleaner look
    title_style = styles['Heading1']
    link_style = ParagraphStyle('link', parent=styles['Normal'], textColor=colors.blue, fontSize=8)
    summary_style = styles['Normal']
    
    elements = []
    elements.append(Paragraph(f"TechCrunch Intelligence Brief - {datetime.now().strftime('%d %b %Y')}", title_style))
    elements.append(Spacer(1, 12))

    for url, summary in summaries:
        elements.append(Paragraph(f"<b>SOURCE:</b> {url}", link_style))
        elements.append(Spacer(1, 5))
        elements.append(Paragraph(summary.replace('\n', '<br/>'), summary_style))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<hr/>", styles['Normal'])) # Horizontal line

    doc.build(elements)
    return filename

# send_email function remains the same
