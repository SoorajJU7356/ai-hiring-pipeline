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
    CREATE TABLE IF NOT EXISTS selected_candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            candidate_email TEXT NOT NULL,
            role_title TEXT NOT NULL,
            domain_relevance_score INTEGER,
            experience_score INTEGER,
            skills_match_score INTEGER,
            weighted_score REAL,
            reasoning TEXT,
            matched_skills TEXT,
            skill_gaps TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rejected_candidates(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT NOT NULL,
            candidate_email TEXT NOT NULL,
            role_title TEXT NOT NULL,
            domain_relevance_score INTEGER,
            experience_score INTEGER,
            skills_match_score INTEGER,
            weighted_score REAL,
            reasoning TEXT,
            matched_skills TEXT,
            skill_gaps TEXT,
            created_at TEXT NOT NULL
            )
    """)
    conn.commit()
    conn.close()


def save_selected_candidate(
    candidate_name: str,
    candidate_email:str,
    role_title: str,
    domain_relevance_score: int,
    experience_score:int,
    skills_match_score:int,
    weighted_score:float,
    reasoning: str,
    matched_skills:str,
    skill_gaps:str
) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO selected_candidates (
            candidate_name, candidate_email,role_title, 
            domain_relevance_score, experience_score, skills_match_score,
            weighted_score, reasoning, matched_skills, skill_gaps,
            created_at
        ) VALUES (?,?,?,?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_name, candidate_email, role_title,
        domain_relevance_score, experience_score, skills_match_score,
        weighted_score, reasoning, matched_skills, skill_gaps,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    run_id = cursor.lastrowid
    conn.close()
    return run_id

def save_rejected_candidate(
    candidate_name: str,
    candidate_email: str,
    role_title: str,
    domain_relevance_score: int,
    experience_score: int,
    skills_match_score: int,
    weighted_score: float,
    reasoning: str,
    matched_skills: str,
    skill_gaps: str
) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rejected_candidates (
            candidate_name, candidate_email, role_title,
            domain_relevance_score, experience_score, skills_match_score,
            weighted_score, reasoning, matched_skills, skill_gaps, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        candidate_name, candidate_email, role_title,
        domain_relevance_score, experience_score, skills_match_score,
        weighted_score, reasoning, matched_skills, skill_gaps,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    run_id = cursor.lastrowid
    conn.close()
    return run_id

def get_selected_candidates() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM selected_candidates ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_rejected_candidates() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rejected_candidates ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_selected_candidate(candidate_id: int)-> bool:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM selected_candidates WHERE id=?", (candidate_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount >0

def delete_rejected_candidate(candidate_id:int) ->bool:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM rejected_candidates WHERE id =?",(candidate_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount>0

def delete_all_selected() -> bool:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM  selected_candidates")
    conn.commit()
    conn.close()
    return True

def delete_all_rejected() -> bool:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM rejected_candidates")
    conn.commit()
    conn.close()
    return True