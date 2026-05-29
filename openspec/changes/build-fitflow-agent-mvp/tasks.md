## 1. Project Setup

- [ ] 1.1 Confirm the MVP scope follows YAGNI/KISS: FastAPI backend, deterministic mock provider, structured response models, sample data, tests, and optional Streamlit UI only. Do not add scraping, authentication, database persistence, embeddings, or multi-agent orchestration.
- [ ] 1.2 Create the Python project structure for the FastAPI app, optional Streamlit UI, tests, samples, and documentation.
- [ ] 1.3 Add dependency and environment configuration files for FastAPI, Pydantic, Uvicorn, pytest, python-dotenv, optional Streamlit, and optional LLM provider support.

## 2. Backend API

- [ ] 2.1 Implement Pydantic request and response models for fit analysis, missing skills, strengths, and preparation plan items.
- [ ] 2.2 Implement a health endpoint and fit-analysis endpoint in FastAPI.
- [ ] 2.3 Validate empty or missing job posting and candidate profile inputs with clear API errors.

## 3. Analysis Workflow

- [ ] 3.1 Implement an LLM provider interface with deterministic mock provider support.
- [ ] 3.2 Implement the fit-analysis service that builds the prompt, invokes the selected provider, validates structured output, and returns the API response model.
- [ ] 3.3 Add real-provider configuration hooks without requiring external credentials for demo or test runs.

## 4. Samples and UI

- [ ] 4.1 Add sample job posting and candidate profile input files.
- [ ] 4.2 Add a sample structured output file matching the response schema.
- [ ] 4.3 Implement the optional Streamlit UI that submits inputs to the FastAPI endpoint and renders the structured result.

## 5. Tests and Documentation

- [ ] 5.1 Add backend tests for health checks, valid fit analysis, validation errors, and deterministic demo mode.
- [ ] 5.2 Add documentation for setup, environment variables, running the API, running tests, running the optional UI, and calling the API with sample data.
- [ ] 5.3 Verify the documented commands work from a clean local setup path.
