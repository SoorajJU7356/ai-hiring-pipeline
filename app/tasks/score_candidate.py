from crewai import Task
from app.agents.scoring_agent import create_scoring_agent

def create_score_candidate_task() -> Task:
    return Task(
        description=(
            "Using the job requirements from the JD analysis and the candidate profile "
            "from the resume screening, evaluate the candidate using these three metrics:\n\n"
            "1. Domain Relevance (weight: 40%) — How closely does the candidate's past work "
            "and experience match the industry and domain of this role? Score 0-10.\n\n"
            "2. Experience Level (weight: 35%) — How well does the candidate's total years "
            "and depth of experience match what the role requires? Score 0-10.\n\n"
            "3. Skills Match (weight: 25%) — How many of the required skills does the "
            "candidate have? Score 0-10.\n\n"
            "Calculate the weighted score as:\n"
            "(Domain x 0.40 + Experience x 0.35 + Skills x 0.25) x 10\n\n"
            "Important: A candidate with high domain relevance should not be filtered out "
            "just because their experience is slightly below the requirement."
        ),
        expected_output=(
            "Return ONLY a JSON object, no other text, in exactly this shape:\n"
            "{\n"
            '  "domain_relevance_score": <0-10>,\n'
            '  "experience_score": <0-10>,\n'
            '  "skills_match_score": <0-10>,\n'
            '  "weighted_score": <0-100>,\n'
            '  "reasoning": "<2-3 sentences covering domain, experience, skills>",\n'
            '  "matched_skills": ["<skill>", "..."],\n'
            '  "skill_gaps": ["<skill>", "..."]\n'
            "}\n"
            "No markdown, no code fences, no text before or after the JSON."
        ),
        agent=create_scoring_agent()
    )