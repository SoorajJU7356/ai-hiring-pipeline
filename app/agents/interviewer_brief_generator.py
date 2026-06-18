from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def create_interviewer_brief_generator() -> Agent:
    return Agent(
        role="Interviewer Brief Generator",
        goal=(
            "Compile a concise, structured interviewer brief for the candidate "
            "including their profile summary, fit score, skill gaps, and interview questions."
        ),
        backstory=(
            "You are a preparation specialist who ensures interviewers walk into every "
            "session fully informed. You summarize clearly and highlight what matters most — "
            "the interviewer should need nothing else besides your brief."
        ),
        llm=llm,
        verbose=True
    )