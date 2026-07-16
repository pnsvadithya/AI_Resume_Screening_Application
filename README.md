# AI Resume Screening

A web application that screens a candidate's resume against a job description using an AI model.
Upload a PDF resume, paste or upload the job description, and get a match score, matched and
missing skills, extracted resume details, strengths, areas for improvement, and a summary.
Every analysis is saved so past results can be reopened from the history page.

## Features

- Upload a PDF resume and validate it before processing
- Paste a job description or upload it as a `.txt` file
- Extract candidate name, email, phone, skills, education, work experience, projects and certifications
- AI analysis with match score, matched skills, missing skills, strengths, areas for improvement and a summary
- Star rating and fit status
- Candidate history stored in SQLite, with each past report re-openable

## Tech Stack

- Python and Flask
- HTML, CSS and Bootstrap
- SQLite
- Groq API (Llama model)

## Requirements

- Python 3.10 or newer
- A free Groq API key from https://console.groq.com

## Setup

Follow these steps to run the application on your system.

### 1. Get the code

```
git clone https://github.com/pnsvadithya/AI_Resume_Screening_Application.git
cd AI_Resume_Screening_Application
```

### 2. Create and activate a virtual environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```
python3 -m venv venv
source venv/bin/activate
```

Once activated, your terminal prompt starts with `(venv)`.

### 3. Install the dependencies

```
pip install -r requirements.txt
```

### 4. Add your Groq API key

Create a file named `.env` in the project root (you can copy `.env.example`) and add:

```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
SECRET_KEY=change-this-to-any-random-string
```

Get a free key at https://console.groq.com (Sign in, open API Keys, create a key).

### 5. Run the application

```
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Usage

1. On the home page, upload a resume from `sample_resumes/` (or your own PDF).
2. Paste a job description from `sample_jds/`, or upload the `.txt` file.
3. Click **Analyze Resume** to view the result.
4. Open **History** to see all past analyses, and click any candidate to reopen the full report.

## Project Structure

```
app.py                 Flask routes and application setup
schema.sql             Database table definition
requirements.txt       Python dependencies
.env.example           Template for the environment file
utils/
    parser.py          PDF text extraction and contact details
    ai.py              Groq API call and response handling
    matcher.py         Star rating and fit status
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

## Notes

- The database file (`database/resume.db`) and uploaded resumes are created automatically and are not tracked by git.
- Keep your `.env` file private. It is ignored by git so it is never committed.
