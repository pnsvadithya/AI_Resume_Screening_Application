import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from utils.ai import analyze_resume
from utils.database import get_all_analyses, get_analysis, init_db, save_analysis
from utils.matcher import fit_status, skill_coverage, star_rating
from utils.parser import parse_resume

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
app.config["UPLOAD_FOLDER"] = "uploads"

init_db()

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def read_job_description(form, files):
    pasted = form.get("job_description", "").strip()
    if pasted:
        return pasted

    jd_file = files.get("jd_file")
    if jd_file and jd_file.filename:
        return jd_file.read().decode("utf-8", errors="ignore").strip()

    return ""


@app.context_processor
def inject_helpers():
    return {"fit_status": fit_status, "star_rating": star_rating}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/history")
def history():
    analyses = get_all_analyses()
    return render_template("history.html", analyses=analyses)


@app.route("/analysis/<int:analysis_id>")
def view_analysis(analysis_id):
    record = get_analysis(analysis_id)
    if not record:
        flash("That analysis could not be found.")
        return redirect(url_for("history"))

    candidate = {
        "name": record["candidate_name"],
        "email": record["email"],
        "phone": record["phone"],
    }
    return render_template(
        "result.html",
        candidate=candidate,
        filename=record["resume_filename"],
        analysis=record,
        rating=star_rating(record["match_score"]),
        fit=fit_status(record["match_score"]),
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files.get("resume")

    if not resume or resume.filename == "":
        flash("Please choose a resume file to upload.")
        return redirect(url_for("index"))

    if not allowed_file(resume.filename):
        flash("Only PDF resumes are supported.")
        return redirect(url_for("index"))

    job_description = read_job_description(request.form, request.files)
    if not job_description:
        flash("Please paste a job description or upload a .txt file.")
        return redirect(url_for("index"))

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    filename = secure_filename(resume.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    resume.save(filepath)

    candidate = parse_resume(filepath)
    analysis = analyze_resume(candidate["text"], job_description)

    rating = star_rating(analysis["match_score"])
    fit = fit_status(analysis["match_score"])
    coverage = skill_coverage(analysis["matched_skills"], analysis["missing_skills"])

    save_analysis(
        candidate["name"],
        candidate["email"],
        candidate["phone"],
        filename,
        analysis["match_score"],
        analysis["matched_skills"],
        analysis["missing_skills"],
        analysis["strengths"],
        analysis["improvements"],
        analysis["summary"],
    )

    return render_template(
        "result.html",
        candidate=candidate,
        filename=filename,
        analysis=analysis,
        rating=rating,
        fit=fit,
        coverage=coverage,
    )


if __name__ == "__main__":
    app.run(debug=True)
