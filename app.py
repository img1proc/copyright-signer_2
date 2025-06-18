from flask import Flask, render_template, request, send_file, redirect, url_for, after_this_request
import os, tempfile, base64

from utils.pdf_generator import generate_pdf_from_html
from utils.crypto import generate_keys, sign_pdf
##1. app.py（step1 → step2まで対応）250618_19_10
app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir()
PDF_FILENAME = "copyright_transfer.pdf"
PDF_PATH = os.path.join(UPLOAD_FOLDER, PDF_FILENAME)

@app.route("/", methods=["GET", "POST"])
def step1():
    title = request.args.get("title", "(No Title Provided)")

    if request.method == "POST":
        author_name = request.form["author_name"]
        affiliation = request.form["affiliation"]
        address = request.form["address"]
        date = request.form["date"]

        html = render_template("pdf_template.html",
                               title=title,
                               author_name=author_name,
                               affiliation=affiliation,
                               address=address,
                               date=date)
        generate_pdf_from_html(html, PDF_PATH)

        return redirect(url_for("step2"))

    return render_template("step1.html", title=title)

@app.route("/sign")
def step2():
    sig_path = os.path.join(UPLOAD_FOLDER, "signature.bin")
    pub_path = os.path.join(UPLOAD_FOLDER, "public_key.pem")
    priv_path = os.path.join(UPLOAD_FOLDER, "private_key.pem")

    try:
        # 秘密鍵・公開鍵生成
        private_key, _ = generate_keys(UPLOAD_FOLDER)

        # PDFハッシュ計算＋署名
        hash_value, signature = sign_pdf(private_key, PDF_PATH, sig_path)
        signature_b64 = base64.b64encode(signature).decode()

        return render_template("step2.html",
                               hash_value=hash_value,
                               signature_b64=signature_b64,
                               files={
                                   "pdf": PDF_FILENAME,
                                   "signature": "signature.bin",
                                   "public_key": "public_key.pem",
                                   "private_key": "private_key.pem"
                               })
    except Exception as e:
        return f"Error during signing: {e}", 500

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    @after_this_request
    def delete_file(response):
        try:
            os.remove(file_path)
        except Exception:
            pass
        return response

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)