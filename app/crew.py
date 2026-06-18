from crewai import Crew, Process
from app.tasks.analyze_jd import create_analyze_jd_task
from app.tasks.screen_resume import create_screen_resume_task
from app.tasks.score_candidate import create_score_candidate_task
from app.tasks.generate_questions import create_generate_questions_task
from app.tasks.draft_email import create_draft_email_task
from app.tasks.generate_brief import create_generate_brief_task

def run_hiring_pipeline(
        jd_text: str,
        resume_text: str,
        candidate_name: str,
        role_title: str,
        shortlisted:bool
) -> dict:
    t1=create_analyze_jd_task(jd_text)
    t2=create_screen_resume_task(resume_text)
    t3= create_score_candidate_task()
    t4=create_generate_questions_task()
    t5=create_draft_email_task(candidate_name,role_title, shortlisted)
    t6= create_generate_brief_task(role_title)

    crew= Crew(
        agents=[t1.agent, t2.agent, t3.agent,t4.agent, t5.agent, t6.agent ],
        tasks=[t1,t2,t3,t4,t5,t6],
        process=Process.sequential,
        verbose=True
    )

    result=crew.kickoff()

    return {
        "jd_analysis": t1.output.raw if t1.output else "",
        "candidate_profile": t2.output.raw if t2.output else "",
        "score_report":t3.output.raw if t3.output else "",
        "interview_questions": t4.output.raw if t4.output else "",
        "email_draft": t5.output.raw if t5.output else "",
        "interviewer_brief": t6.output.raw if t6.output else "",
    }

