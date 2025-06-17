from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generate_pdf(author_name, affiliation, address, date, title, output_path, logo_path=None):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    if logo_path and os.path.exists(logo_path):
        c.drawImage(logo_path, 50, height - 100, width=100, preserveAspectRatio=True)

    y = height - 150
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Copyright Transfer Agreement")

    y -= 40
    c.setFont("Helvetica", 11)
    lines = [
        f"Title of the Paper: {title}",
        "",
        "I hereby transfer to the publisher the copyright of the work described above.",
        "This includes all rights to publish, distribute, and archive the paper.",
        "",
        f"Author Name: {author_name}",
        f"Affiliation: {affiliation}",
        f"Address: {address}",
        f"Date: {date}",
    ]

    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.save()