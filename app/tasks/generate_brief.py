from crewai import Task
from app.agents.interviewer_brief_generator import create_interviewer_brief_generator

def create_generate_brief_task(role_title: str) -> Task:
    return Task(
        description=(
            f"Compile a complete interviewer brief for the candidate applying for {role_title}. "
            f"Use all information gathered by previous agents: "
            f"the candidate profile, fit score, skill gaps, and interview questions.\n\n"
            f"The brief should allow an interviewer to walk into the session "
            f"fully prepared without reading the raw resume."
        ),
        expected_output=(
            "A structured interviewer brief containing:\n"
            "- Candidate Summary (name, current role, total experience)\n"
            "- Role Applied For\n"
            "- Fit Score and Reasoning\n"
            "- Matched Skills\n"
            "- Skill Gaps to Probe\n"
            "- Interview Questions (organized by type)\n"
            "- Suggested Focus Areas for the Interview"
        ),
        agent=create_interviewer_brief_generator()
    )