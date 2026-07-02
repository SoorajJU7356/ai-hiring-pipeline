import streamlit as st
import requests
import pandas as pd
import json
import os

API_URL = "http://127.0.0.1:8000"
SETTINGS_PATH = "settings.json"
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

if "settings_key" not in st.session_state:
    st.session_state["settings_key"] = 0

st.set_page_config(page_title="AI Hiring Pipeline", layout="wide")

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            return json.load(f)
    return {"sender_name": "", "gmail_address": "", "app_password": ""}

def save_settings(data):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f)

# Top bar with title and settings button
title_col, settings_col = st.columns([8, 1])
with title_col:
    st.title("AI Hiring Pipeline")
with settings_col:
    st.write("")
    st.write("")
    if st.button("⚙️ Settings"):
        st.session_state["show_settings"] = not st.session_state.get("show_settings", False)

# Settings panel (right-aligned using columns)
if st.session_state.get("show_settings", False):
    _, settings_panel = st.columns([2, 1])
    with settings_panel:
        st.markdown("### ⚙️ Email Settings")
        st.divider()

        current = load_settings()

        sender_name = st.text_input("Sender Name", value="", placeholder="e.g. HR Team - TechCorp", key=f"sender_name_{st.session_state['settings_key']}")
        company_name = st.text_input("Company Name", value="", placeholder="e.g. TechCorp", key=f"company_name_{st.session_state['settings_key']}")
        gmail_address = st.text_input("Gmail Address", value="", placeholder="yourname@gmail.com", key=f"gmail_address_{st.session_state['settings_key']}")
        app_password = st.text_input("App Password", value="", type="password", placeholder="xxxx xxxx xxxx xxxx", key=f"app_password_{st.session_state['settings_key']}")

        st.divider()
        with st.expander("How to get your App Password"):
            st.markdown("""
**Step 1 — Enable 2-Step Verification**
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** in the left sidebar
3. Under *How you sign in to Google*, enable **2-Step Verification**

**Step 2 — Generate App Password**
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Sign in again if prompted
3. Fill **App Name**.
4. Click **Create**
5. Copy the 16-character password shown

**Step 3 — Paste it above**
Enter your Gmail address and the App Password in the fields above and click Save.

> ⚠️ Never share your App Password with anyone.
            """)

        if st.button("Save Settings", type="primary", use_container_width=True):
            save_settings({
                "sender_name": sender_name,
                "company_name": company_name,
                "gmail_address": gmail_address,
                "app_password": app_password
            })
            st.session_state["settings_key"] += 1
            st.session_state["show_settings"] = False
            st.success("Settings saved successfully.")
            st.rerun()

        if st.button("Close", use_container_width=True):
            st.session_state["show_settings"] = False
            st.rerun()

st.divider()
if not os.path.exists("settings.json"):
    st.warning("Email not configured. Please click Settings and enter your Gmail credentials before running the pipeline.")
tab1, tab2, tab3, tab4 = st.tabs([
    "Single Candidate",
    "Bulk Screening",
    "Selected Candidates",
    "Rejected Candidates"
])

with tab1:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste the job description here", height=200, key="single_jd")

    st.subheader("Resume")
    resume_pdf = st.file_uploader("Upload candidate's resume (PDF)",type=["pdf"],key=f"single_resume_{st.session_state['uploader_key']}")
    if st.button("Run Scoring Pipeline", type="primary"):
        if not jd_text or resume_pdf is None:
            st.error("Please provide both the job description and resume PDF.")
        else:
            with st.spinner("Agents are analyzing the candidate... this may take 30-60 seconds."):
                response = requests.post(
                    f"{API_URL}/score",
                    data={"jd_text": jd_text},
                    files={"resume_pdf": (resume_pdf.name, resume_pdf.getvalue(), "application/pdf")}
                )
            if response.status_code == 200:
                result = response.json()
                st.session_state["score_result"] = result
                st.session_state["uploader_key"] += 1
                st.rerun()
            else:
                st.error(f"Pipeline failed: {response.text}")

    if "score_result" in st.session_state:
        result = st.session_state["score_result"]

        st.divider()
        st.subheader("Candidate Identified")
        col1, col2, col3 = st.columns(3)
        col1.info(f"**Name:** {result.get('candidate_name', 'Not found')}")
        col2.info(f"**Email:** {result.get('candidate_email', 'Not found')}")
        col3.info(f"**Role:** {result.get('role_title', 'Not found')}")

        st.subheader("Scoring Results")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Domain Relevance", f"{result['domain_relevance_score']}/10")
        col2.metric("Experience Level", f"{result['experience_score']}/10")
        col3.metric("Skills Match", f"{result['skills_match_score']}/10")
        col4.metric("Weighted Score", f"{result['weighted_score']}/100")

        st.subheader("Reasoning")
        st.info(result["reasoning"])

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Matched Skills")
            st.success(result["matched_skills"])
        with col_b:
            st.subheader("Skill Gaps")
            st.warning(result["skill_gaps"])

        st.divider()
        st.subheader("Human Review")
        st.write("Review the scoring above and make your decision:")

        col_accept, col_reject = st.columns(2)
        with col_accept:
            if st.button("Accept — Send Interview Invite", type="primary", use_container_width=True):
                with st.spinner("Drafting and sending interview invitation..."):
                    decide_response = requests.post(
                        f"{API_URL}/decide",
                        data={**result, "accepted": True}
                    )
                if decide_response.status_code == 200:
                    st.success("Candidate accepted. Interview invitation sent successfully.")
                    del st.session_state["score_result"]
                    st.rerun()
                else:
                    st.error(f"Error: {decide_response.text}")

        with col_reject:
            if st.button("Reject — Send Rejection Email", use_container_width=True):
                with st.spinner("Drafting and sending rejection email..."):
                    decide_response = requests.post(
                        f"{API_URL}/decide",
                        data={**result, "accepted": False}
                    )
                if decide_response.status_code == 200:
                    st.warning("Candidate rejected. Polite rejection email sent.")
                    del st.session_state["score_result"]
                    st.rerun()
                else:
                    st.error(f"Error: {decide_response.text}")

with tab2:
    st.subheader("Job Description")
    bulk_jd = st.text_area("Paste the job description here", height=200, key="bulk_jd")

    st.subheader("Resumes")
    bulk_pdfs = st.file_uploader(
                "Upload multiple resume PDFs",
                type=["pdf"],
                accept_multiple_files=True,
                key=f"bulk_resumes_{st.session_state['uploader_key']}"
            )

    if st.button("Run Bulk Scoring", type="primary"):
        if not bulk_jd or not bulk_pdfs:
            st.error("Please provide a job description and at least one resume PDF.")
        else:
            results = []
            progress = st.progress(0, text="Starting bulk scoring...")
            total = len(bulk_pdfs)

            for i, pdf in enumerate(bulk_pdfs):
                progress.progress(
                    i / total,
                    text=f"Scoring resume {i+1} of {total}: {pdf.name}"
                )
                response = requests.post(
                    f"{API_URL}/score",
                    data={"jd_text": bulk_jd},
                    files={"resume_pdf": (pdf.name, pdf.getvalue(), "application/pdf")}
                )
                if response.status_code == 200:
                    results.append(response.json())
                else:
                    st.warning(f"Failed to score {pdf.name}: {response.text}")

            progress.progress(1.0, text="All resumes scored.")
            st.session_state["uploader_key"] += 1
            st.session_state["bulk_results"] = results

    if "bulk_results" in st.session_state:
        bulk_results = st.session_state["bulk_results"]

        st.divider()
        st.subheader("Review Candidates")
        st.write("Check the box to accept a candidate. Unchecked means reject.")

        # Table headers
        h1, h2, h3, h4, h5, h6, h7, h8 = st.columns([2, 2, 1, 1, 1, 1, 3, 1])
        h1.markdown("**Name**")
        h2.markdown("**Email**")
        h3.markdown("**Domain**")
        h4.markdown("**Experience**")
        h5.markdown("**Skills**")
        h6.markdown("**Weighted**")
        h7.markdown("**Reasoning & Gaps**")
        h8.markdown("**Accept**")
        st.divider()

        decisions = {}
        for i, r in enumerate(bulk_results):
            c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([2, 2, 1, 1, 1, 1, 3, 1])
            c1.write(r.get("candidate_name", "Unknown"))
            c2.write(r.get("candidate_email", ""))
            c3.metric("", f"{r.get('domain_relevance_score', 0)}/10")
            c4.metric("", f"{r.get('experience_score', 0)}/10")
            c5.metric("", f"{r.get('skills_match_score', 0)}/10")
            c6.metric("", f"{r.get('weighted_score', 0)}/100")
            c7.write(r.get("reasoning", ""))
            c7.caption(f"Gaps: {r.get('skill_gaps', '')}")
            decisions[i] = c8.checkbox("", key=f"accept_{i}")
            st.divider()

        if st.button("Submit Decisions", type="primary"):
            success_count = 0
            fail_count = 0
            with st.spinner("Processing decisions and sending emails..."):
                for i, r in enumerate(bulk_results):
                    accepted = decisions[i]
                    decide_response = requests.post(
                        f"{API_URL}/decide",
                        data={**r, "accepted": accepted}
                    )
                    if decide_response.status_code == 200:
                        success_count += 1
                    else:
                        fail_count += 1

            st.success(f"Decisions submitted. {success_count} emails sent successfully.")
            if fail_count:
                st.warning(f"{fail_count} emails failed to send.")
            del st.session_state["bulk_results"]
            st.rerun()

with tab3:
    st.subheader("Selected Candidates")

    col_refresh, col_download, col_delete_all = st.columns([1, 1, 1])
    with col_refresh:
        if st.button("Refresh", key="refresh_selected"):
            st.rerun()

    response = requests.get(f"{API_URL}/selected")
    selected = response.json() if response.status_code == 200 else []

    if selected:
        df = pd.DataFrame(selected)
        display_cols = [
            "candidate_name", "candidate_email", "role_title",
            "domain_relevance_score", "experience_score", "skills_match_score",
            "weighted_score", "reasoning", "matched_skills", "skill_gaps", "created_at"
        ]
        df = df[[c for c in display_cols if c in df.columns]]

        with col_download:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="selected_candidates.csv",
                mime="text/csv"
            )

        with col_delete_all:
            if st.button("Delete All", key="delete_all_selected", type="secondary"):
                st.session_state["confirm_delete_all_selected"] = True

        if st.session_state.get("confirm_delete_all_selected"):
            st.warning("Are you sure you want to delete all selected candidates? This cannot be undone.")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("Yes, Delete All", key="confirm_yes_selected", type="primary"):
                    requests.delete(f"{API_URL}/selected")
                    st.session_state["confirm_delete_all_selected"] = False
                    st.rerun()
            with col_no:
                if st.button("Cancel", key="confirm_no_selected"):
                    st.session_state["confirm_delete_all_selected"] = False
                    st.rerun()

        for c in selected:
            with st.expander(f"{c['candidate_name']} — {c['role_title']} — Score: {c['weighted_score']}"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Domain Relevance", f"{c['domain_relevance_score']}/10")
                col2.metric("Experience Level", f"{c['experience_score']}/10")
                col3.metric("Skills Match", f"{c['skills_match_score']}/10")
                col4.metric("Weighted Score", f"{c['weighted_score']}/100")
                st.write(f"**Email:** {c['candidate_email']}")
                st.write(f"**Reasoning:** {c['reasoning']}")
                st.write(f"**Matched Skills:** {c['matched_skills']}")
                st.write(f"**Skill Gaps:** {c['skill_gaps']}")
                st.caption(f"Processed on: {c['created_at']}")
                st.divider()
                if st.button("Delete", key=f"delete_selected_{c['id']}", type="secondary"):
                    requests.delete(f"{API_URL}/selected/{c['id']}")
                    st.rerun()
    else:
        st.info("No selected candidates yet.")

with tab4:
    st.subheader("Rejected Candidates")

    col_refresh, col_download, col_delete_all = st.columns([1, 1, 1])
    with col_refresh:
        if st.button("Refresh", key="refresh_rejected"):
            st.rerun()

    response = requests.get(f"{API_URL}/rejected")
    rejected = response.json() if response.status_code == 200 else []

    if rejected:
        df = pd.DataFrame(rejected)
        display_cols = [
            "candidate_name", "candidate_email", "role_title",
            "domain_relevance_score", "experience_score", "skills_match_score",
            "weighted_score", "reasoning", "matched_skills", "skill_gaps", "created_at"
        ]
        df = df[[c for c in display_cols if c in df.columns]]

        with col_download:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="rejected_candidates.csv",
                mime="text/csv"
            )

        with col_delete_all:
            if st.button("Delete All", key="delete_all_rejected", type="secondary"):
                st.session_state["confirm_delete_all_rejected"] = True

        if st.session_state.get("confirm_delete_all_rejected"):
            st.warning("Are you sure you want to delete all rejected candidates? This cannot be undone.")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("Yes, Delete All", key="confirm_yes_rejected", type="primary"):
                    requests.delete(f"{API_URL}/rejected")
                    st.session_state["confirm_delete_all_rejected"] = False
                    st.rerun()
            with col_no:
                if st.button("Cancel", key="confirm_no_rejected"):
                    st.session_state["confirm_delete_all_rejected"] = False
                    st.rerun()

        for c in rejected:
            with st.expander(f"{c['candidate_name']} — {c['role_title']} — Score: {c['weighted_score']}"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Domain Relevance", f"{c['domain_relevance_score']}/10")
                col2.metric("Experience Level", f"{c['experience_score']}/10")
                col3.metric("Skills Match", f"{c['skills_match_score']}/10")
                col4.metric("Weighted Score", f"{c['weighted_score']}/100")
                st.write(f"**Email:** {c['candidate_email']}")
                st.write(f"**Reasoning:** {c['reasoning']}")
                st.write(f"**Matched Skills:** {c['matched_skills']}")
                st.write(f"**Skill Gaps:** {c['skill_gaps']}")
                st.caption(f"Processed on: {c['created_at']}")
                st.divider()
                if st.button("Delete", key=f"delete_rejected_{c['id']}", type="secondary"):
                    requests.delete(f"{API_URL}/rejected/{c['id']}")
                    st.rerun()
    else:
        st.info("No rejected candidates yet.")