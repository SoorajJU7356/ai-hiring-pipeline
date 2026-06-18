from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def create_interview_question_generator() -> Agent:
    return Agent(
        role="Interview Question Generator",
        goal=(
            "Generate tailored interview questions for the candidate based on "
            "their skill gaps, experience level, and the role requirements."
        ),
        backstory=(
            "You are a senior technical interviewer who crafts precise, role-specific questions. "
            "You focus on skill gaps identified in scoring, and mix behavioral, "
            "technical, and situational questions appropriate for the role level."
        ),
        llm=llm,
        verbose=True
    )