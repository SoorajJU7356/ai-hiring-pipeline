# AI Hiring Pipeline

An end-to-end AI-powered hiring pipeline that automates candidate screening, scoring, and communication — built with CrewAI, Groq, FastAPI, and Streamlit.

---

## What is this?

The AI Hiring Pipeline is a multi-agent system that helps HR teams screen job applicants efficiently. Instead of manually reading through resumes and writing emails, the pipeline automates the heavy lifting — parsing resumes, scoring candidates against job requirements, and drafting professional emails — while keeping a human in the loop for the final hiring decision.

The system supports both single candidate screening and bulk resume processing, making it suitable for high-volume hiring scenarios.

---

## How it works

1. HR uploads a job description and one or more resume PDFs
2. AI agents analyze the JD and resumes in parallel
3. A scoring agent evaluates each candidate using a weighted metric system
4. The HR reviewer sees a breakdown of scores and reasoning
5. HR clicks Accept or Reject for each candidate
6. The system automatically sends a professional email to the candidate
7. The candidate's details are saved to the database

---

## Agent Architecture

The pipeline uses 4 specialized CrewAI agents, each with a distinct role:

### Agent 1 — JD Analyst
Reads the job description and extracts structured information including the role title, required skills, preferred skills, years of experience needed, education requirements, and key responsibilities. This agent runs in parallel with the Resume Screener to save time.

### Agent 2 — Resume Screener
Parses the candidate's resume PDF and extracts a structured profile including the candidate's name, email address, current role, total years of experience, skills, work history, education, and certifications. Also runs in parallel with the JD Analyst.

### Agent 3 — Scoring Agent
Receives the structured outputs from both the JD Analyst and Resume Screener and evaluates the candidate using three weighted metrics. Produces a score from 0 to 100 with bullet-point reasoning for each metric, a list of matched skills, and identified skill gaps.

### Agent 4 — Communication Agent
Triggered only after the HR reviewer makes a decision. Drafts a professional, personalized email — either a warm interview invitation for accepted candidates or a polite, empathetic rejection email. Uses the HR user's name and company name from settings for the sign-off.

---

## Scoring System

Candidates are evaluated on three weighted metrics:

| Metric | Weight | What it measures |
|---|---|---|
| Domain Relevance | 40% | How closely the candidate's background matches the role's industry and domain |
| Experience Level | 35% | How well the candidate's years and depth of experience match the requirement |
| Skills Match | 25% | How many of the required skills the candidate possesses |

**Weighted Score Formula:**
(Domain × 0.40 + Experience × 0.35 + Skills × 0.25) × 10
Domain relevance is intentionally weighted highest — a candidate with strong domain experience but slightly fewer years will score higher than one with more years in an unrelated field. This reflects real-world hiring priorities.

---

## Human-in-the-Loop

After scoring, the HR reviewer sees:
- Per-metric scores (Domain, Experience, Skills)
- Overall weighted score out of 100
- Bullet-point reasoning for each metric
- Matched skills and skill gaps

The human makes the final call. No email is sent and nothing is saved to the database until the HR reviewer explicitly clicks Accept or Reject.

---

## Features

- **Single candidate screening** — upload one resume, get instant scoring and review
- **Bulk resume screening** — upload multiple PDFs, score all at once, review in a table with checkboxes
- **Parallel agent execution** — JD Analyst and Resume Screener run simultaneously, cutting pipeline time in half
- **Auto-extraction** — candidate name, email, and role title are extracted automatically from the resume and JD
- **Professional email drafting** — emails are personalized, warm, and never mention scores or rejection reasons
- **Separate candidate databases** — selected and rejected candidates stored in separate SQLite tables
- **CSV export** — download selected or rejected candidates as a CSV file
- **Delete candidates** — delete individual candidates or clear entire tables
- **Settings panel** — HR users can configure their Gmail credentials directly from the UI without touching code
- **App Password tutorial** — step-by-step guide built into the settings panel

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — LLaMA 3.3 70B (free tier) |
| Agent Framework | CrewAI |
| Frontend | Streamlit |
| Backend | FastAPI |
| PDF Parsing | pypdf |
| Email | Gmail SMTP via smtplib |
| Database | SQLite |
| Package Manager | uv |

---

## Project Structure
ai-hiring-pipeline/
├── app/
│   ├── agents/
│   │   ├── init.py
│   │   ├── jd_analyst.py
│   │   ├── resume_screener.py
│   │   ├── scoring_agent.py
│   │   └── communication_agent.py
│   ├── tasks/
│   │   ├── init.py
│   │   ├── analyze_jd.py
│   │   ├── screen_resume.py
│   │   ├── score_candidate.py
│   │   └── draft_email.py
│   ├── utils/
│   │   ├── init.py
│   │   ├── database.py
│   │   ├── email_sender.py
│   │   └── pdf_extractor.py
│   ├── crew.py
│   └── main.py
├── streamlit_app.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md

---

## Setup

### Prerequisites
- Python 3.12
- uv package manager — https://docs.astral.sh/uv
- A Groq API key — https://console.groq.com
- A Gmail account with App Password (for sending emails)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/SoorajJU7356/ai-hiring-pipeline.git
cd ai-hiring-pipeline
```

**2. Install dependencies**
```bash
uv sync
```

**3. Set up environment variables**
```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:
GROQ_API_KEY=your_groq_api_key_here
CREWAI_TRACING_ENABLED=false

**4. Start the backend**
```bash
uv run python -m uvicorn app.main:app --reload --port 8000
```

**5. Start the frontend** (in a new terminal)
```bash
uv run python -m streamlit run streamlit_app.py
```

**6. Open the app**

Go to `http://localhost:8501` in your browser.

**7. Configure email**

Click the **Settings** button in the top right, enter your name, company name, Gmail address, and App Password. A built-in tutorial guides you through generating an App Password if you haven't done it before.

---

## Environment Variables

Only one variable is required to run the pipeline:
GROQ_API_KEY=your_groq_api_key_here
CREWAI_TRACING_ENABLED=false

Email credentials are configured via the Settings panel in the UI and stored locally in `settings.json` (never committed to git).

---

## Database

Two SQLite tables are maintained locally in `hiring_pipeline.db`:

**selected_candidates** — candidates approved by the HR reviewer
**rejected_candidates** — candidates rejected by the HR reviewer

Both tables store:
- Candidate name and email
- Role applied for
- Domain relevance, experience, and skills match scores
- Weighted score
- Reasoning (bullet points)
- Matched skills and skill gaps
- Timestamp

---

## Notes

- The pipeline runs entirely locally — no cloud infrastructure needed
- All tools used are free (Groq free tier, SQLite, Gmail SMTP)
- `settings.json` and `hiring_pipeline.db` are excluded from git via `.gitignore`
- The system is single-user — the last saved Settings credentials are used for all emails
