CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    resume_filename TEXT,
    match_score INTEGER,
    matched_skills TEXT,
    missing_skills TEXT,
    strengths TEXT,
    improvements TEXT,
    summary TEXT,
    created_at TEXT NOT NULL
);
