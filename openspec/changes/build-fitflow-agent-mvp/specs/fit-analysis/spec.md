## ADDED Requirements

### Requirement: Submit fit analysis request
The system SHALL accept a job posting and candidate profile as user-provided text and return a fit analysis response.

#### Scenario: Valid text input
- **WHEN** a request includes non-empty `job_posting` and `candidate_profile` values
- **THEN** the system returns a successful analysis response containing a fit score, summary, strengths, missing skills, and preparation plan

#### Scenario: Missing required text
- **WHEN** a request omits `job_posting` or `candidate_profile`, or provides an empty value
- **THEN** the system rejects the request with validation feedback

### Requirement: Produce structured fit assessment
The system SHALL produce a structured assessment with a numeric fit score, a concise summary, matched strengths, missing skills, and rationale suitable for portfolio demonstration.

#### Scenario: Successful assessment
- **WHEN** the analysis provider completes successfully
- **THEN** the response includes a fit score from 0 to 100, at least one strength, at least one missing skill or gap, and a short explanation of the assessment

### Requirement: Generate prioritized preparation plan
The system SHALL generate a preparation plan prioritized by expected impact on the candidate's readiness for the target role.

#### Scenario: Preparation plan returned
- **WHEN** the system identifies candidate gaps for a job posting
- **THEN** the response includes ordered preparation items with priority, action, reason, and suggested time investment

### Requirement: Support deterministic demo mode
The system SHALL support a deterministic demo mode that returns sample-quality analysis without requiring external LLM credentials.

#### Scenario: Demo run without API key
- **WHEN** the application runs with demo or mock provider configuration
- **THEN** fit analysis succeeds without making a network call to an external LLM provider

### Requirement: Support optional Streamlit UI
The system SHALL provide an optional Streamlit UI that lets a user paste inputs, submit analysis, and view the structured result.

#### Scenario: UI analysis flow
- **WHEN** a user enters a job posting and candidate profile in the Streamlit UI and submits the form
- **THEN** the UI calls the FastAPI analysis endpoint and displays the score, summary, strengths, missing skills, and preparation plan

### Requirement: Include beginner-friendly samples and documentation
The system SHALL include sample inputs, sample output, and documentation that explain setup, configuration, local usage, API usage, and UI usage.

#### Scenario: Reviewer follows documentation
- **WHEN** a new reviewer opens the project documentation
- **THEN** they can identify how to install dependencies, run the API, run the optional UI, and execute a sample analysis
