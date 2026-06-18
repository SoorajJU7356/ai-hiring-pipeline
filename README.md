# AI Hiring Pipeline

An end-to-end AI-powered hiring pipeline built with CrewAI, Groq (LLaMA 3.3 70B), Streamlit, and FastAPI.

## What it does
- Analyzes job descriptions and candidate resumes
- Scores candidates against role requirements (0-100)
- Generates tailored interview questions based on skill gaps
- Drafts personalized emails (invite or rejection)
- Produces a structured interviewer brief PDF

## Architecture
6 specialized CrewAI agents running sequentially:
1. JD Analyst
2. Resume Screener
3. Scoring Agent
4. Interview Question Generator
5. Communication Agent
6. Interviewer Brief Generator

## Tech Stack
- **LLM**: Groq (LLaMA 3.3 70B) — free tier
- **Agent Framework**: CrewAI
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **PDF Generation**: ReportLab
- **Email**: Gmail SMTP
- **Storage**: SQLite + local filesystem
- **Package Manager**: uv

## Setup
1. Clone the repo
2. Install uv
3. Run `uv sync`
4. Copy `.env.example` to `.env` and fill in your keys
5. Run `uv run streamlit run app/main.py`

## Environment Variables
See `.env.example` for required keys.