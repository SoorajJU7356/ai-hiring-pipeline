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
            "Evaluate the candidate against the job requirements using three weighted metrics:"
            "Domain Relevance (40%), Experience Level(35%), and Skills Match(25%)."
            "Score each metric from 1 to 10 and calculate the final score out of 100"
        ),
        backstory=(
            "You are an analytical hiring specialist who evaluates candidates using a structured "
            "scoring framework. You never guess — you score based only on evidence found in the "
            "resume versus the job requirements. You prioritize domain relevance above all else, "
            "meaning a candidate with strong domain background but slightly less experience "
            "should score higher than a candidate with more experience in an unrelated domain."
        ),
        llm=llm,
        verbose=True
    )