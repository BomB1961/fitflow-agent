# FitFlow Agent

FitFlow Agent is a beginner-friendly AI/LLM portfolio MVP. It compares a job posting with a candidate profile, identifies strengths and missing skills, and returns a prioritized preparation plan.

The default provider is deterministic mock mode, so tests and local demos do not require real API credentials.

## Scope

Included:

- FastAPI backend
- Deterministic mock provider by default
- Structured Pydantic response models
- Sample job posting, candidate profile, and output
- Backend tests
- Optional Streamlit UI
- Optional OpenAI-compatible provider configuration

Not included:

- Scraping
- Authentication
- Database persistence
- Embeddings or vector search
- Multi-agent orchestration

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,ui]"
```

Copy `.env.example` to `.env` if you want to customize provider settings. The default provider is `mock`.

## Run the API

```powershell
uvicorn app.main:app --reload
```

Open the interactive API docs at `http://localhost:8000/docs`.

## Run a Sample Analysis

```powershell
$body = @{
  job_posting = Get-Content -Raw samples/job_posting.txt
  candidate_profile = Get-Content -Raw samples/candidate_profile.txt
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/analyze -ContentType "application/json" -Body $body
```

Expected output shape is shown in `samples/sample_output.json`.

## Run Tests

```powershell
pytest
```

## Optional Streamlit UI

Start the API first, then run:

```powershell
streamlit run ui/streamlit_app.py
```

The UI calls `http://localhost:8000` by default. Set `FITFLOW_API_URL` to point at a different API URL.

## Optional OpenAI-Compatible Provider

Mock mode is recommended for tests and portfolio demos. To try a real OpenAI-compatible API manually:

```powershell
$env:FITFLOW_LLM_PROVIDER = "openai"
$env:OPENAI_API_KEY = "<your-api-key>"
$env:OPENAI_MODEL = "gpt-4o-mini"
uvicorn app.main:app --reload
```

Real API credentials are never required for tests or local demo runs.
