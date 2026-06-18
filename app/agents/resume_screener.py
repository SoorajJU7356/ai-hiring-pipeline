from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def create_resume_screener() -> Agent:
    return Agent(
        role="Resume Screener",
        goal=(
            "Parse the candidate's resume and extract a structured profile "
            "including skills, work experience, education, and certifications."
        ),
        backstory=(
            "You are a meticulous recruiter who has screened thousands of resumes. "
            "You extract factual information without bias, organizing it clearly "
            "so other agents can compare it against job requirements."
        ),
        llm=llm,
        verbose=True
    )