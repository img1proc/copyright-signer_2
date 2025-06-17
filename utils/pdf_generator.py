from weasyprint import HTML
import os
## 修正構成：HTML → PDF → 署名（cryptography） :📄 1. utils/pdf_generator.py（WeasyPrint版）
def generate_pdf_from_html(html_content, output_path):
    HTML(string=html_content, base_url=os.getcwd()).write_pdf(output_path)
base_url=os.getcwd() 
##により画像（<img src="...">）もPDF内に正しく埋め込まれます。
