from crewai import Crew, Process
from app.tasks.analyze_jd import create_analyze_jd_task
from app.tasks.screen_resume import create_screen_resume_task
from app.tasks.score_candidate import create_score_candidate_task
import re


def extract_field(text: str, label: str) -> str:
    match = re.search(rf"{label}:\s*([^\n]+)", text)
    return match.group(1).strip() if match else ""


def parse_score_report(report: str) -> dict:
    domain = extract_field(report, "DOMAIN_RELEVANCE_SCORE")
    experience = extract_field(report, "EXPERIENCE_SCORE")
    skills = extract_field(report, "SKILLS_MATCH_SCORE")
    weighted = extract_field(report, "WEIGHTED_SCORE")
    reasoning = extract_field(report, "REASONING")
    matched = extract_field(report, "MATCHED_SKILLS")
    gaps = extract_field(report, "SKILL_GAPS")

    return {
        "domain_relevance_score": int(domain) if domain.isdigit() else 0,
        "experience_score": int(experience) if experience.isdigit() else 0,
        "skills_match_score": int(skills) if skills.isdigit() else 0,
        "weighted_score": float(weighted) if weighted else 0.0,
        "reasoning": reasoning,
        "matched_skills": matched,
        "skill_gaps": gaps
    }


def run_scoring_pipeline(
    jd_text: str,
    resume_text: str,
) -> dict:

    t1 = create_analyze_jd_task(jd_text)
    t2 = create_screen_resume_task(resume_text)
    t1.async_execution = True
    t2.async_execution = True

    t3 = create_score_candidate_task()

    crew = Crew(
        agents=[t1.agent, t2.agent, t3.agent],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True
    )

    crew.kickoff()

    jd_output = t1.output.raw if t1.output else ""
    resume_output = t2.output.raw if t2.output else ""
    raw_report = t3.output.raw if t3.output else ""

    parsed_scores = parse_score_report(raw_report)

    role_title = extract_field(jd_output, "ROLE_TITLE")
    candidate_name = extract_field(resume_output, "CANDIDATE_NAME")
    candidate_email = extract_field(resume_output, "CANDIDATE_EMAIL")

    return {
        "candidate_name": candidate_name,
        "candidate_email": candidate_email,
        "role_title": role_title,
        "jd_analysis": jd_output,
        "candidate_profile": resume_output,
        "raw_score_report": raw_report,
        **parsed_scores
    }