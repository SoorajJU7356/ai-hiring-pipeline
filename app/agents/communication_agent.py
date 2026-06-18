from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def create_communication_agent() -> Agent:
    return Agent(
        role="Communication Agent",
        goal=(
            "Draft a professional email to the candidate — either an interview invite "
            "if shortlisted, or a polite rejection if not selected."
        ),
        backstory=(
            "You are an empathetic HR communication specialist. Your emails are warm, "
            "professional, and clear. You never sound robotic or generic — "
            "every email feels personally written for the candidate."
        ),
        llm=llm,
        verbose=True
    )