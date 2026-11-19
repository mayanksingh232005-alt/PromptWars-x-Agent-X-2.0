# AgentFlow AI — Agentic Workflow Automation

**Challenge:** PS01 — Agentic Workflow Automation

AgentFlow AI is a small, deployable prototype that turns a natural-language goal into an explainable multi-step workflow. It demonstrates a planner, a safe executor, run tracking, and human-in-the-loop safeguards.

## Features
- Natural-language goal input
- Intent-aware workflow planning
- Ordered task list with execution statuses
- Safe demo executor (does not send messages, delete data, purchase items, or publish content)
- Human approval flag for sensitive/external actions
- JSON API and health endpoint
- Dockerfile for Google Cloud Run

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```
Open http://127.0.0.1:8000

## API
- `GET /` — web interface
- `POST /api/run` — create and execute a workflow
- `GET /health` — health check

Example:
```bash
curl -X POST http://127.0.0.1:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"goal":"Research three CRM tools and prepare a comparison report"}'
```

## Deploy to Google Cloud Run
From this directory, with Google Cloud CLI installed and authenticated:
```bash
gcloud run deploy agentflow-ai \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated
```
Cloud Run prints the deployed HTTPS URL. Use that exact URL in the hackathon form.

## Safety note
This prototype simulates safe workflow execution. It does not claim to connect to external apps or perform real-world actions. Sensitive actions are explicitly flagged for human approval. Extend it with authenticated integrations and permission-scoped tools before enabling real execution.

## Evaluation alignment
- Code quality: modular planning and execution functions
- Security: no secrets, no arbitrary shell execution, no external side effects
- Efficiency: lightweight FastAPI service
- Testing: health endpoint and API workflow can be tested
- Accessibility: responsive page, clear labels, keyboard-usable textarea/button
- Problem alignment: goal decomposition, task execution, and approval checkpoint
