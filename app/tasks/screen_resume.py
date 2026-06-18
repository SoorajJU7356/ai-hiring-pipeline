from crewai import Task
from app.agents.resume_screener import create_resume_screener

def create_screen_resume_task(resume_text: str) -> Task:
    return Task(
        description=(
            f"Parse the following resume and extract a structured candidate profile:\n\n"
            f"{resume_text}\n\n"
            f"Extract: candidate name, current role, total years of experience, "
            f"skills, work history, education, and certifications."
        ),
        expected_output=(
            "A structured candidate profile with the following sections:\n"
            "- Candidate Name\n"
            "- Current Role\n"
            "- Total Experience\n"
            "- Skills (list)\n"
            "- Work History (list with role, company, duration)\n"
            "- Education\n"
            "- Certifications (list)"
        ),
        agent=create_resume_screener()
    )