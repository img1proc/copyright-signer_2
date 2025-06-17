from flask import Flask, render_template, request, send_file, after_this_request
from flask import render_template_string
import os, tempfile
import base64

from utils.crypto import generate_keys, sign_pdf
from utils.pdf_generator import generate_pdf_from_html

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    hash_value = None
    signature_b64 = None
    files = {}
    error = None

    # 論文タイトル取得（クエリ文字列）
    title = request.args.get("title", "(No Title Provided)")

    if request.method == "POST":
        # フォームから著者情報取得
        author_name = request.form.get("author_name")
        affiliation = request.form.get("affiliation")
        address = request.form.get("address")
        date = request.form.get("date")

        # 出力ファイルパス
        pdf_path = os.path.join(UPLOAD_FOLDER, "copyright_transfer.pdf")
        sig_path = os.path.join(UPLOAD_FOLDER, "signature.bin")
        pub_path = os.path.join(UPLOAD_FOLDER, "public_key.pem")
        priv_path = os.path.join(UPLOAD_FOLDER, "private_key.pem")

        try:
            # 1. HTMLテンプレートを文字列として描画
            html_content = render_template("pdf_template.html",
                                           author_name=author_name,
                                           affiliation=affiliation,
                                           address=address,
                                           date=date,
                                           title=title)

            # 2. HTML → PDF変換（WeasyPrint）
            generate_pdf_from_html(html_content, pdf_path)

            # 3. 秘密鍵・公開鍵生成
            private_key, _ = generate_keys(UPLOAD_FOLDER)

            # 4. PDFをハッシュ化 → 署名ファイル出力
            hash_value, signature = sign_pdf(private_key, pdf_path, sig_path)
            signature_b64 = base64.b64encode(signature).decode()

            # 5. ダウンロード用ファイル情報
            files = {
                "pdf": "copyright_transfer.pdf",
                "signature": "signature.bin",
                "public_key": "public_key.pem",
                "private_key": "private_key.pem"
            }

        except Exception as e:
            error = str(e)

        return render_template("index.html",
                               hash_value=hash_value,
                               signature_b64=signature_b64,
                               files=files,
                               title=title,
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