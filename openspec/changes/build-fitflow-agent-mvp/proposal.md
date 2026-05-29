## Why

Beginner AI/LLM portfolio projects need a clear, useful workflow that demonstrates prompt design, structured LLM output, backend API design, and simple product documentation. FitFlow Agent will provide a focused MVP that helps a user compare a job posting with a candidate profile and turn the gap analysis into an actionable preparation plan.

## What Changes

- Add a FastAPI backend that accepts a job posting and candidate profile as text input.
- Use an LLM-backed analysis flow to produce a fit score, supporting rationale, matching strengths, missing skills, and prioritized preparation steps.
- Include deterministic sample inputs and sample output so the project can be understood and demonstrated without first connecting a paid LLM provider.
- Add an optional Streamlit UI for local portfolio demos.
- Add beginner-friendly documentation covering setup, configuration, API usage, sample runs, and project structure.

## Capabilities

### New Capabilities
- `fit-analysis`: Analyze a job posting and candidate profile, identify fit signals and skill gaps, and generate a prioritized preparation plan.

### Modified Capabilities

## Impact

- New application code for a FastAPI service, LLM adapter, analysis workflow, schemas, and optional Streamlit UI.
- New sample data and documentation for local demonstration.
- New Python dependencies for API serving, validation, environment configuration, optional UI, and LLM integration.
