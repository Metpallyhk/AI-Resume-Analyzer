from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():

    extracted_text = ""

    if request.method == "POST":

        if "resume" not in request.files:
            extracted_text = "No file selected."
            return render_template("index.html", text=extracted_text)

        file = request.files["resume"]

        if file.filename == "":
            extracted_text = "Please select a file."

        elif not file.filename.lower().endswith(".pdf"):
            extracted_text = "Only PDF files are allowed."

        else:

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            try:
                reader = PdfReader(filepath)

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        extracted_text += page_text

            except Exception:
                extracted_text = "Unable to extract text from this PDF."

    return render_template("index.html", text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True)
