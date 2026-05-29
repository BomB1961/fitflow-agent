import os

import requests
import streamlit as st


API_URL = os.getenv("FITFLOW_API_URL", "http://localhost:8000")


st.set_page_config(page_title="FitFlow Agent", page_icon=":briefcase:")
st.title("FitFlow Agent")

job_posting = st.text_area("Job posting", height=260)
candidate_profile = st.text_area("Candidate profile", height=220)

if st.button("Analyze fit", type="primary"):
    try:
        response = requests.post(
            f"{API_URL.rstrip('/')}/analyze",
            json={
                "job_posting": job_posting,
                "candidate_profile": candidate_profile,
            },
            timeout=30,
        )
    except requests.RequestException as exc:
        st.error(
            "Could not connect to the FitFlow API. "
            "Start the FastAPI server first or check FITFLOW_API_URL."
        )
        st.code(str(exc))
        st.stop()

    if response.ok:
        result = response.json()
        st.metric("Fit score", f"{result['fit_score']}/100")
        st.subheader("Summary")
        st.write(result["summary"])
        st.subheader("Rationale")
        st.write(result["rationale"])

        st.subheader("Strengths")
        for item in result["strengths"]:
            st.markdown(f"- **{item['skill']}**: {item['evidence']}")

        st.subheader("Missing skills")
        for item in result["missing_skills"]:
            st.markdown(f"- **{item['skill']}** ({item['importance']}): {item['why_it_matters']}")

        st.subheader("Preparation plan")
        for item in result["preparation_plan"]:
            st.markdown(
                f"{item['priority']}. **{item['action']}** "
                f"({item['suggested_time']}) - {item['reason']}"
            )
    else:
        st.error(f"Request failed: {response.status_code}")
        st.code(response.text)
