from crewai import Task
from app.agents.scoring_agent import create_scoring_agent

def create_score_candidate_task() -> Task:
    return Task(
        description=(
            "Using the job requirements from the JD analysis and the candidate profile "
            "from the resume screening, evaluate the candidate's fit for the role.\n\n"
            "Compare skills, experience, and qualifications. "
            "Identify what matches, what is missing, and what is partially met."
        ),
        expected_output=(
            "A scoring report with:\n"
            "- Overall Fit Score (0-100)\n"
            "- Score Reasoning (2-3 sentences)\n"
            "- Matched Skills (list)\n"
            "- Missing Skills (list)\n"
            "- Partial Matches (list)\n"
            "- Recommendation: Shortlist or Reject"
        ),
        agent=create_scoring_agent()
    )