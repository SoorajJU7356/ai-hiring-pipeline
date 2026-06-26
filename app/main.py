from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.crew import run_scoring_pipeline
from app.tasks.draft_email import create_draft_email_task
from app.utils.email_sender import send_email, parse_email_draft
from app.utils.pdf_extractor import extract_text_from_pdf
from app.utils.database import (
    init_db,
    save_selected_candidate,
    save_rejected_candidate,
    get_selected_candidates,
    get_rejected_candidates
)
from crewai import Crew, Process
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Hiring Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

init_db()


@app.post("/score")
async def score_candidate(
    jd_text: str = Form(...),
    resume_pdf: UploadFile = File(...)
):
    pdf_bytes = await resume_pdf.read()
    resume_text = extract_text_from_pdf(pdf_bytes)

    result = run_scoring_pipeline(
        jd_text=jd_text,
        resume_text=resume_text
    )
    return result


@app.post("/decide")
async def decide(
    candidate_name: str = Form(...),
    candidate_email: str = Form(...),
    role_title: str = Form(...),
    domain_relevance_score: int = Form(...),
    experience_score: int = Form(...),
    skills_match_score: int = Form(...),
    weighted_score: float = Form(...),
    reasoning: str = Form(...),
    matched_skills: str = Form(...),
    skill_gaps: str = Form(...),
    accepted: bool = Form(...)
):
    task = create_draft_email_task(candidate_name, role_title, accepted)
    crew = Crew(
        agents=[task.agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    crew.kickoff()
    email_text = task.output.raw if task.output else ""
    parsed = parse_email_draft(email_text)

    email_result = send_email(
        to_email=candidate_email,
        subject=parsed["subject"],
        body=parsed["body"]
    )

    if accepted:
        save_selected_candidate(
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            role_title=role_title,
            domain_relevance_score=domain_relevance_score,
            experience_score=experience_score,
            skills_match_score=skills_match_score,
            weighted_score=weighted_score,
            reasoning=reasoning,
            matched_skills=matched_skills,
            skill_gaps=skill_gaps
        )
    else:
        save_rejected_candidate(
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            role_title=role_title,
            domain_relevance_score=domain_relevance_score,
            experience_score=experience_score,
            skills_match_score=skills_match_score,
            weighted_score=weighted_score,
            reasoning=reasoning,
            matched_skills=matched_skills,
            skill_gaps=skill_gaps
        )

    return {
        "email_sent": email_result["success"],
        "email_message": email_result["message"],
        "decision": "accepted" if accepted else "rejected"
    }


@app.get("/selected")
def list_selected():
    return get_selected_candidates()


@app.get("/rejected")
def list_rejected():
    return get_rejected_candidates()


@app.get("/health")
def health():
    return {"status": "ok"}