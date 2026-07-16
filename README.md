# AI Resume Screening

A web application that screens a candidate's resume against a job description using an AI model.
Upload a PDF resume, paste or upload the job description, and get a match score, matched and
missing skills, strengths, areas for improvement, suggestions, and an AI summary. Every analysis
is saved so you can review past results in the history page.

## Features

- Upload a PDF resume and validate it before processing
- Paste a job description or upload it as a `.txt` file
- Extract candidate name, email, and phone from the resume
- AI analysis with match score, matched skills, missing skills, strengths, improvements, suggestions and a summary
- Star rating, fit status and a skill coverage progress bar
- Candidate history stored in SQLite

## Tech Stack

- Python and Flask
- HTML, CSS and Bootstrap
- SQLite
- Groq API (Llama model)

## Project Structure

```
app.py                 Flask routes and application setup
schema.sql             Database table definition
requirements.txt       Python dependencies
utils/
    parser.py          PDF text extraction and contact details
    ai.py              Groq API call and response handling
    matcher.py         Star rating, fit status and skill coverage
    database.py        SQLite setup, save and retrieve
templates/
    index.html         Upload page
    result.html        Analysis result page
    history.html       Candidate history page
static/
    style.css          Custom styles
sample_resumes/        Example PDF resumes
sample_jds/            Example job descriptions
```

## Setup

1. Create and activate a virtual environment.

   ```
   python -m venv venv
   venv\Scripts\activate        (Windows)
   source venv/bin/activate     (macOS / Linux)
   ```

2. Install the dependencies.

   ```
   pip install -r requirements.txt
   ```

3. Get a free Groq API key from https://console.groq.com and create a `.env` file
   in the project root (you can copy `.env.example`):

   ```
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   SECRET_KEY=change-this-to-any-random-string
   ```

## Running

```
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Usage

1. On the home page, upload a resume from `sample_resumes/` (or your own PDF).
2. Paste a job description from `sample_jds/`, or upload the `.txt` file.
3. Click **Analyze Resume** to view the result.
4. Open **History** to see all past analyses.
