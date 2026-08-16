from flask import Flask, render_template, request
from pdf import extract_text_from_pdf
from skill_extractor import extract_skills
from matches import calculate_match_score

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        resume = request.files["resume"]
        job_description = request.form["job_description"]

        resume_text = extract_text_from_pdf(resume)

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        matched_skills = [
            skill for skill in resume_skills
            if skill in job_skills
        ]

        missing_skills = [
            skill for skill in job_skills
            if skill not in resume_skills
        ]

        score = calculate_match_score(
            resume_text,
            job_description
        )

        return render_template(
            "result.html",
            score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
