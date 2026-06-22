# Clinical Note Agent

A FastAPI service that analyzes unstructured clinical notes and extracts structured output
including SOAP format, ICD-10 code suggestions, and clinical risk flags — without logging
protected health information.

## What it does

POST a raw clinical note, receive:

- **SOAP note** (Subjective, Objective, Assessment, Plan)
- **ICD-10 codes** with confidence scores
- **Risk flags** (fall risk, medication concerns, follow-up urgency)
- **Follow-up recommendations**

PHI safety: raw note text is never written to logs. Only structured output and metadata
are recorded.

## Stack

Python 3.11, FastAPI, Pydantic, Docker, GitHub Actions

## Run locally

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

POST to `http://localhost:8000/analyze`:

```json
{
  "note_text": "Patient is a 58-year-old male presenting with 3-day history of chest pain..."
}
```

## Deploy

Docker image is built and pushed to ECR on every merge to main via GitHub Actions.
