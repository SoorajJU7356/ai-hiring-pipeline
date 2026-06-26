# AI Hiring Pipeline

An end-to-end AI-powered hiring pipeline built with CrewAI, Groq (LLaMA 3.3 70B), Streamlit, and FastAPI.

## What it does
- Analyzes job descriptions and candidate resumes in parallel
- Scores candidates using a weighted metric-based system
- Escalates to a human reviewer with score breakdown and reasoning
- Sends professional emails (interview invite or rejection) based on human decision
- Stores selected and rejected candidates in separate local databases

## Scoring System
Candidates are evaluated on three weighted metrics:

| Metric | Weight |
|---|---|
| Domain Relevance | 40% |
| Experience Level | 35% |
| Skills Match | 25% |

Domain relevance is prioritized — a candidate with strong domain background
but slightly less experience will score higher than one with more experience
in an unrelated domain.

## Architecture
4 specialized CrewAI agents:

1. **JD Analyst** — extracts requirements from the job description
2. **Resume Screener** — parses and structures the candidate profile
3. **Scoring Agent** — evaluates candidate using weighted metrics
4. **Communication Agent** — drafts invite or rejection email based on human decision

Agents 1 and 2 run in parallel. Agent 3 runs after both complete.
Agent 4 runs only after human approves or rejects.

## Human-in-the-Loop
After scoring, a popup appears in the UI showing:
- Per-metric scores
- Weighted total score
- Reasoning
- Accept / Reject buttons

The human makes the final call. The pipeline only sends emails and saves
to the database after the human decision is made.

## Tech Stack
- **LLM**: Groq (LLaMA 3.3 70B) — free tier
- **Agent Framework**: CrewAI
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Email**: Gmail SMTP
- **Storage**: SQLite (two separate tables for selected and rejected candidates)
- **Package Manager**: uv

## Project Structure
ai-hiring-pipeline/

├── app/

│   ├── agents/

│   │   ├── jd_analyst.py

│   │   ├── resume_screener.py

│   │   ├── scoring_agent.py

│   │   └── communication_agent.py

│   ├── tasks/

│   │   ├── analyze_jd.py

│   │   ├── screen_resume.py

│   │   ├── score_candidate.py

│   │   └── draft_email.py

│   ├── utils/

│   │   ├── database.py

│   │   └── email_sender.py

│   ├── crew.py

│   └── main.py

├── outputs/

├── .env.example

├── pyproject.toml

└── README.md

## Setup
1. Clone the repo
2. Install uv — https://docs.astral.sh/uv
3. Run `uv sync`
4. Copy `.env.example` to `.env` and fill in your keys
5. Start the backend: `uv run uvicorn app.main:app --reload --port 8000`
6. Start the frontend: `uv run streamlit run streamlit_app.py`

## Environment Variables
GROQ_API_KEY=your_groq_api_key_here

GMAIL_SENDER=your_gmail@gmail.com

GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

CREWAI_TRACING_ENABLED=false

## Database
Two SQLite tables are maintained locally:
- `selected_candidates` — candidates approved by the human reviewer
- `rejected_candidates` — candidates rejected by the human reviewer

Both tables store: candidate name, email, role, metric scores, weighted score,reasoning, matched skills, and skill gaps.