import json
import os

from groq import Groq

DEFAULT_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are an expert technical recruiter. You compare a candidate's resume "
    "against a job description and return a strict, honest evaluation as JSON."
)

USER_TEMPLATE = """Analyze the resume against the job description and respond with a single JSON object.

Job Description:
{job_description}

Resume:
{resume_text}

Return JSON with exactly these keys:
- "match_score": integer from 0 to 100
- "matched_skills": array of skills found in both the resume and the job description
- "missing_skills": array of important skills in the job description but absent from the resume
- "strengths": array of short strings describing the candidate's strengths
- "improvements": array of short strings describing areas to improve
- "suggestions": array of short, practical resume suggestions
- "summary": a concise paragraph explaining why the candidate is or is not a good fit

Base the match_score on how well the resume covers the job description. Respond with JSON only."""


def _empty_result(summary):
    return {
        "match_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "strengths": [],
        "improvements": [],
        "suggestions": [],
        "summary": summary,
    }


def _normalize(data):
    result = _empty_result("")
    result["summary"] = str(data.get("summary", "")).strip()

    try:
        score = int(round(float(data.get("match_score", 0))))
    except (TypeError, ValueError):
        score = 0
    result["match_score"] = max(0, min(100, score))

    for key in ("matched_skills", "missing_skills", "strengths", "improvements", "suggestions"):
        value = data.get(key, [])
        if isinstance(value, list):
            result[key] = [str(item).strip() for item in value if str(item).strip()]
    return result


def analyze_resume(resume_text, job_description):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _empty_result("AI is not configured. Set GROQ_API_KEY in the .env file.")

    prompt = USER_TEMPLATE.format(
        job_description=job_description.strip(),
        resume_text=resume_text.strip(),
    )

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", DEFAULT_MODEL),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        data = json.loads(response.choices[0].message.content)
        return _normalize(data)
    except Exception as error:
        return _empty_result(f"Could not analyze the resume right now: {error}")
