import os

import requests
import streamlit as st


API_URL = os.getenv("FITFLOW_API_URL", "http://localhost:8000")

SAMPLE_JOB_POSTING = """Fitness coaching app developer

We need a junior AI application developer to build a small workout planning tool.

Responsibilities:
- Build Python FastAPI endpoints with typed request and response models.
- Create simple LLM prompts for fitness notes and parse structured JSON.
- Add pytest coverage for happy paths and validation errors.
- Create a Streamlit demo that non-technical reviewers can try quickly."""

SAMPLE_CANDIDATE_PROFILE = """- Built a Python workout tracker that stores exercise notes and weekly goals.
- Created FastAPI endpoints with Pydantic models for typed responses.
- Wrote pytest tests for API health checks and form validation.
- Used Streamlit to demo progress summaries and simple preparation tips.
- Interested in prompt design for coaching and fitness habit feedback."""


st.set_page_config(page_title="FitFlow Agent", page_icon=":briefcase:")
st.title("FitFlow Agent")
st.write(
    "FitFlow Agent compares a role or project brief with candidate notes, "
    "then returns strengths, missing skills, and a prioritized preparation plan."
)
st.caption(
    "The default mock provider is deterministic, so this demo works without API keys. "
    "The sample is fitness-themed, but you can replace it with your own job, project, "
    "workout, or portfolio notes."
)

job_posting = st.text_area("Role or project brief", value=SAMPLE_JOB_POSTING, height=260)
candidate_profile = st.text_area(
    "Candidate or project notes",
    value=SAMPLE_CANDIDATE_PROFILE,
    height=220,
)

st.caption("Click Analyze fit to send these notes to the local FastAPI backend and render the structured result.")
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
        st.subheader("Analysis result")
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
