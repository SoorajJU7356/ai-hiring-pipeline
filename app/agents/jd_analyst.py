from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def create_jd_analyst() -> Agent:
    return Agent(
        role="Job Description Analyst",
        goal=(
            "Extract and structure all key requirements from a job description "
            "including required skills, experience level, qualifications, and responsibilities."
        ),
        backstory=(
            "You are an expert HR analyst with 10 years of experience breaking down "
            "job descriptions. You identify both explicit requirements and implicit expectations. "
            "You output clean, structured information that other agents can easily use."
        ),
        llm=llm,
        verbose=True
    )