## Context

FitFlow Agent starts from an empty repository with OpenSpec configured. The MVP should be small enough for a beginner portfolio while still showing practical AI application skills: API design, structured LLM prompting, validation, fallback sample data, and documentation.

The core workflow is a single analysis request: a user provides a job posting and candidate profile, the system analyzes fit with an LLM or deterministic mock provider, and the system returns a structured assessment plus a prioritized preparation plan.

## Goals / Non-Goals

**Goals:**
- Provide a FastAPI backend with a health endpoint and a fit-analysis endpoint.
- Keep LLM integration replaceable through a small provider interface so local demos can use mock output.
- Return structured JSON that is stable enough for tests, documentation, and a Streamlit UI.
- Include sample inputs, sample output, and beginner-friendly setup instructions.
- Keep project structure understandable for someone reviewing an AI/LLM portfolio project.

**Non-Goals:**
- User accounts, authentication, persistence, or multi-user history.
- Resume parsing from PDF/DOCX files.
- Automated job-board scraping.
- Fine-tuning, embeddings, vector search, or agent tool orchestration.
- Production deployment hardening beyond basic configuration notes.

## Decisions

1. Use FastAPI with Pydantic request and response models.
   - Rationale: FastAPI gives beginner-friendly API docs, type validation, and a clear path for testing.
   - Alternative considered: Flask. Flask is simpler at first glance, but would require more manual validation and documentation work.

2. Create an `LLMProvider` abstraction with `MockLLMProvider` and `OpenAILLMProvider` style implementations.
   - Rationale: The app remains demonstrable without API keys while still showing how a real LLM would be connected.
   - Alternative considered: Calling a provider directly from the route. That would be shorter but harder to test and document.

3. Require structured analysis output in a fixed JSON shape.
   - Rationale: Fit score, strengths, gaps, and preparation tasks need to be displayable by the UI and testable by backend tests.
   - Alternative considered: Returning free-form Markdown. That is easier to generate but weaker for product behavior and automated checks.

4. Keep Streamlit optional and API-backed.
   - Rationale: The portfolio can demonstrate both API and UI usage without coupling UI code to backend internals.
   - Alternative considered: Building only Streamlit. That would reduce files, but the FastAPI backend is the stronger reusable foundation.

5. Include a deterministic demo mode as the default path.
   - Rationale: Reviewers can run the project immediately, and tests do not depend on network access or paid API calls.
   - Alternative considered: Requiring a real LLM key for all usage. That creates avoidable setup friction for an MVP.

## Risks / Trade-offs

- LLM output may be malformed or incomplete -> Validate provider responses with Pydantic and return clear errors when real provider output cannot be parsed.
- Fit scores can appear overly authoritative -> Document that results are preparation guidance, not hiring decisions, and include rationale fields.
- Mock output may not reflect real model behavior -> Keep mock output labeled as demo behavior and include sample real-provider configuration.
- Beginner scope can expand quickly -> Keep persistence, file parsing, embeddings, and authentication out of the MVP tasks.

## Migration Plan

This is a new project, so no data migration is required. Implementation can be delivered as a new Python package with documentation and samples. Rollback is removing the added application files and dependencies.

## Resolved Decisions

- Default LLM provider: Use the deterministic mock provider by default. Add only OpenAI-compatible provider hooks as optional configuration. Real API credentials must not be required for tests or local demo runs.
- Sample candidate profile format: Use structured bullet text rather than resume-style prose, because it is easier for reviewers to read and produces more stable demo input.
