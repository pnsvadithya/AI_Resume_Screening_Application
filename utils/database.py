import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join("database", "resume.db")
SCHEMA_PATH = "schema.sql"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _ensure_column(connection, column, column_type):
    columns = [row[1] for row in connection.execute("PRAGMA table_info(analyses)")]
    if column not in columns:
        connection.execute(f"ALTER TABLE analyses ADD COLUMN {column} {column_type}")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema = schema_file.read()
    connection = get_connection()
    connection.executescript(schema)
    _ensure_column(connection, "strengths", "TEXT")
    _ensure_column(connection, "improvements", "TEXT")
    connection.commit()
    connection.close()


def save_analysis(candidate_name, email, phone, resume_filename, match_score,
                  matched_skills, missing_skills, strengths, improvements, summary):
    init_db()
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO analyses
            (candidate_name, email, phone, resume_filename, match_score,
             matched_skills, missing_skills, strengths, improvements, summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            candidate_name,
            email,
            phone,
            resume_filename,
            match_score,
            json.dumps(matched_skills),
            json.dumps(missing_skills),
            json.dumps(strengths),
            json.dumps(improvements),
            summary,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
        ),
    )
    connection.commit()
    connection.close()


def _row_to_dict(row):
    record = dict(row)
    for key in ("matched_skills", "missing_skills", "strengths", "improvements"):
        record[key] = json.loads(record.get(key) or "[]")
    return record


def get_all_analyses():
    init_db()
    connection = get_connection()
    rows = connection.execute("SELECT * FROM analyses ORDER BY id DESC").fetchall()
    connection.close()
    return [_row_to_dict(row) for row in rows]


def get_analysis(analysis_id):
    init_db()
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM analyses WHERE id = ?", (analysis_id,)
    ).fetchone()
    connection.close()
    return _row_to_dict(row) if row else None
