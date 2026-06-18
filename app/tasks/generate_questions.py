from crewai import Task
from app.agents.interview_question_generator import create_interview_question_generator

def create_generate_questions_task() -> Task:
    return Task(
        description=(
            "Based on the candidate's skill gaps and the role requirements identified earlier, "
            "generate tailored interview questions for this specific candidate.\n\n"
            "Include a mix of: technical questions targeting skill gaps, "
            "behavioral questions for the role level, and situational questions "
            "relevant to the key responsibilities."
        ),
        expected_output=(
            "A list of 8-10 interview questions organized as:\n"
            "- Technical Questions (3-4): targeting identified skill gaps\n"
            "- Behavioral Questions (2-3): relevant to role responsibilities\n"
            "- Situational Questions (2-3): real scenarios the candidate may face in this role"
        ),
        agent=create_interview_question_generator()
    )