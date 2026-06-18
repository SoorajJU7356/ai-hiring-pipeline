from app.utils.database import init_db, save_run, get_all_runs

init_db()

run_id = save_run(
    candidate_name="John Doe",
    role_title="Python Developer",
    fit_score=60,
    shortlisted=True,
    pdf_path="outputs/brief_John_Doe_test.pdf",
    email_draft="Subject: Interview Invite\n\nDear John...",
    score_report="Overall Fit Score: 60"
)

print(f"Saved run with ID: {run_id}")

runs = get_all_runs()
print(f"Total runs in DB: {len(runs)}")
print(f"Latest run: {runs[0]['candidate_name']} — {runs[0]['role_title']} — Score: {runs[0]['fit_score']}")