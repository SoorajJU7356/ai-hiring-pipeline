from crewai import Task
from app.agents.jd_analyst import create_jd_analyst

def create_analyze_jd_task(jd_text: str) -> Task:
    return Task(
        description=(
            f"Analyze the following job description and extract structured information:\n\n"
            f"{jd_text}\n\n"
            f"Extract: job title, required skills, preferred skills, "
            f"years of experience required, education requirements, and key responsibilities."
        ),
        expected_output=(
            "A structured summary with the following sections:\n"
            "- Job Title\n"
            "- Required Skills (list)\n"
            "- Preferred Skills (list)\n"
            "- Experience Required\n"
            "- Education Requirements\n"
            "- Key Responsibilities (list)"
        ),
        agent=create_jd_analyst()
    )