from weasyprint import HTML
##utils/pdf_generator.py（WeasyPrintによるPDF生成）:250618_19_10
def generate_pdf_from_html(html_content, output_path):
    HTML(string=html_content).write_pdf(output_path)