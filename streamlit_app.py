import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Hiring Pipeline", layout="wide")
st.title("AI Hiring Pipeline")

tab1, tab2, tab3 = st.tabs(["Run Pipeline", "Selected Candidates", "Rejected Candidates"])

with tab1:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste the job description here", height=200)

    st.subheader("Resume")
    resume_pdf = st.file_uploader("Upload candidate's resume (PDF)", type=["pdf"])

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
    st.subheader("Selected Candidates")
    if st.button("Refresh", key="refresh_selected"):
        st.rerun()
    response = requests.get(f"{API_URL}/selected")
    selected = response.json() if response.status_code == 200 else []
    if selected:
        for c in selected:
            with st.expander(f"{c['candidate_name']} — {c['role_title']} — Score: {c['weighted_score']}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Domain Relevance", f"{c['domain_relevance_score']}/10")
                col2.metric("Experience Level", f"{c['experience_score']}/10")
                col3.metric("Skills Match", f"{c['skills_match_score']}/10")
                st.write(f"**Email:** {c['candidate_email']}")
                st.write(f"**Reasoning:** {c['reasoning']}")
                st.write(f"**Matched Skills:** {c['matched_skills']}")
                st.write(f"**Skill Gaps:** {c['skill_gaps']}")
                st.caption(f"Processed on: {c['created_at']}")
    else:
        st.info("No selected candidates yet.")

with tab3:
    st.subheader("Rejected Candidates")
    if st.button("Refresh", key="refresh_rejected"):
        st.rerun()
    response = requests.get(f"{API_URL}/rejected")
    rejected = response.json() if response.status_code == 200 else []
    if rejected:
        for c in rejected:
            with st.expander(f"{c['candidate_name']} — {c['role_title']} — Score: {c['weighted_score']}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Domain Relevance", f"{c['domain_relevance_score']}/10")
                col2.metric("Experience Level", f"{c['experience_score']}/10")
                col3.metric("Skills Match", f"{c['skills_match_score']}/10")
                st.write(f"**Email:** {c['candidate_email']}")
                st.write(f"**Reasoning:** {c['reasoning']}")
                st.write(f"**Matched Skills:** {c['matched_skills']}")
                st.write(f"**Skill Gaps:** {c['skill_gaps']}")
                st.caption(f"Processed on: {c['created_at']}")
    else:
        st.info("No rejected candidates yet.")