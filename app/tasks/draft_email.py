from crewai import Task
from app.agents.communication_agent import create_communication_agent

def create_draft_email_task(
    candidate_name: str,
    role_title: str,
    accepted: bool,
    sender_name: str = "HR Team",
    company_name: str = ""
) -> Task:
    signoff = f"{sender_name}\nHR\n{company_name}" if company_name else f"{sender_name}\nHR"

    if accepted:
        instruction = (
            f"Draft a warm, professional interview invitation email to {candidate_name} "
            f"for the role of {role_title}. "
            f"Mention that they have been shortlisted after a careful review of their profile. "
            f"Let them know the HR team will follow up shortly with interview details. "
            f"Keep it concise, encouraging, and personal. "
            f"Do not mention any scores or metrics. "
            f"End the email with exactly this sign-off:\n{signoff}"
        )
    else:
        instruction = (
            f"Draft a polite, empathetic rejection email to {candidate_name} "
            f"for the role of {role_title}. "
            f"Thank them sincerely for their time and interest in the role. "
            f"Let them know the team has decided to move forward with other candidates. "
            f"Wish them well in their job search. "
            f"Keep it respectful and warm. "
            f"Do not mention any scores, metrics, or specific reasons for rejection. "
            f"End the email with exactly this sign-off:\n{signoff}"
        )

    return Task(
        description=instruction,
        expected_output=(
            "A complete professional email in exactly this format:\n"
            "SUBJECT: <subject line>\n"
            "BODY:\n"
            "<greeting>\n\n"
            "<body paragraph 1>\n\n"
            "<body paragraph 2>\n\n"
            f"<sign-off exactly as: {signoff}>"
        ),
        agent=create_communication_agent()
    )