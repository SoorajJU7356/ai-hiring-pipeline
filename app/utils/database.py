import sqlite3
import os
from datetime import datetime

DB_PATH = "hiring_pipeline.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
          CREATE TABLE IF NOT EXISTS pipeline_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            role_title TEXT NOT NULL,
            fit_score INTEGER,
            shortlisted BOOLEAN NOT NULL,
            pdf_path TEXT,
            email_draft TEXT,
            score_report TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_run(
    candidate_name: str,
    role_title: str,
    fit_score: int,
    shortlisted: bool,
    pdf_path: str,
    email_draft: str,
    score_report: str
) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pipeline_runs (
            candidate_name, role_title, fit_score,
            shortlisted, pdf_path, email_draft,
            score_report, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_name,
        role_title,
        fit_score,
        shortlisted,
        pdf_path,
        email_draft,
        score_report,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    run_id = cursor.lastrowid
    conn.close()
    return run_id


def get_all_runs() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM pipeline_runs
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_run_by_id(run_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pipeline_runs WHERE id = ?", (run_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None