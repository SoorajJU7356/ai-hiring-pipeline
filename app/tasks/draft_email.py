from crewai import Task
from app.agents.communication_agent import create_communication_agent

def create_draft_email_task(candidate_name: str, role_title: str, shortlisted: bool) -> Task:
    if shortlisted:
        instruction = (
            f"Draft a warm, professional interview invitation email to {candidate_name} "
            f"for the role of {role_title}. "
            f"Mention that they have been shortlisted and will be contacted shortly "
            f"with interview details. Keep it concise and encouraging."
        )
    else:
        instruction = (
            f"Draft a polite, empathetic rejection email to {candidate_name} "
            f"for the role of {role_title}. "
            f"Thank them for their time, wish them well, and keep it respectful. "
            f"Do not mention specific reasons for rejection."
        )

    return Task(
        description=instruction,
        expected_output=(
            "A complete email with:\n"
            "- Subject line\n"
            "- Greeting\n"
            "- Body (2-3 short paragraphs)\n"
            "- Professional sign-off"
        ),
        agent=create_communication_agent()
    )