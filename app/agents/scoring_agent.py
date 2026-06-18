from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def create_scoring_agent() -> Agent:
    return Agent(
        role="Candidate Scoring Agent",
        goal=(
            "Compare the candidate profile against the job requirements and "
            "produce a fit score from 0 to 100 with clear reasoning and identified skill gaps."
        ),
        backstory=(
            "You are an analytical hiring specialist who objectively evaluates candidates. "
            "You never guess — you score based only on evidence found in the resume "
            "versus the requirements extracted from the job description."
        ),
        llm=llm,
        verbose=True
    )