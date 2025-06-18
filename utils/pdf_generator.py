from weasyprint import HTML
import os

def generate_pdf_from_html(html_content, output_path):
    HTML(string=html_content, base_url=os.getcwd()).write_pdf(output_path)