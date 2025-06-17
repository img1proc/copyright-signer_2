from flask import Flask, render_template, request, send_file, after_this_request
import os
import tempfile
import base64

from utils.pdf_generator import generate_pdf
from utils.crypto import generate_keys, sign_pdf

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    hash_value = None
    signature_b64 = None
    error = None
    files = {}

    title = request.args.get("title", "(No Title Provided)")

    if request.method == "POST":
        # 入力データ取得
        author_name = request.form.get("author_name")
        affiliation = request.form.get("affiliation")
        address = request.form.get("address")
        date = request.form.get("date")

        # ファイル名定義
        pdf_filename = "copyright_transfer.pdf"
        sig_filename = "signature.bin"
        pub_filename = "public_key.pem"
        priv_filename = "private_key.pem"

        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
        sig_path = os.path.join(UPLOAD_FOLDER, sig_filename)
        pub_path = os.path.join(UPLOAD_FOLDER, pub_filename)
        priv_path = os.path.join(UPLOAD_FOLDER, priv_filename)

        try:
            # PDF生成
            logo_path = os.path.join("static", "img", "ICAITD_Credit_LOGO.png")
            generate_pdf(author_name, affiliation, address, date, title, pdf_path, logo_path)

            # 鍵生成・署名
            private_key, _ = generate_keys(UPLOAD_FOLDER)
            hash_value, signature = sign_pdf(private_key, pdf_path, sig_path)
            signature_b64 = base64.b64encode(signature).decode()

            files = {
                "pdf": pdf_filename,
                "signature": sig_filename,
                "public_key": pub_filename,
                "private_key": priv_filename,
            }

        except Exception as e:
            error = f"Error during processing: {str(e)}"

        return render_template("index.html", title=title,
                               hash_value=hash_value,
                               signature_b64=signature_b64,
                               files=files,
                               error=error)

    return render_template("index.html", title=title)

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception:
            pass
        return response

    return send_file(file_path, as_attachment=True)