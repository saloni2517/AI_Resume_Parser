from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pathlib import Path
from parser import parse_resume

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx"}

UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return "Please select a resume.", 400

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected.", 400

    if not allowed_file(file.filename):
        return "Only PDF and DOCX files are allowed.", 400

    filename = secure_filename(file.filename)

    if not filename:
        return "Invalid filename.", 400

    file_path = UPLOAD_FOLDER / filename

    try:
        file.save(file_path)

        result = parse_resume(file_path)

        return render_template("results.html", result=result)

    except Exception:
        app.logger.exception("Resume processing failed")
        return (
            "Unable to process this resume. "
            "Please check the file and try again.",
            400
        )

    finally:
        if file_path.exists():
            file_path.unlink()


@app.errorhandler(413)
def file_too_large(error):
    return "File is too large. Maximum size is 5 MB.", 413


if __name__ == "__main__":
    app.run(debug=True)