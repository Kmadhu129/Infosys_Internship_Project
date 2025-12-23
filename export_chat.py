from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime


def export_chat_to_pdf(chat, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title = chat.get("title", "Chat Export")
    created = chat.get("created_at", "")

    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    if created:
        story.append(Paragraph(f"Date: {created}", styles["Normal"]))
    story.append(Spacer(1, 12))

    for msg in chat.get("messages", []):
        role = msg["role"].capitalize()
        content = msg["content"].replace("\n", "<br/>")
        story.append(Paragraph(f"<b>{role}:</b> {content}", styles["Normal"]))
        story.append(Spacer(1, 10))

    doc.build(story)
