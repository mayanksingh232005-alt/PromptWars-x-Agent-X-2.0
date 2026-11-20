
# AgentFlow AI
### PS01 – Agentic Workflow Automation

AgentFlow AI is a workflow automation prototype that converts natural-language goals into structured, explainable workflows.

## Problem Statement

Users often have complex tasks that require planning, execution, monitoring and safety checks. AgentFlow AI demonstrates how an agentic workflow system can organize these tasks into manageable steps.

## Key Features

- Natural-language goal input
- Automatic task classification
- Structured workflow planning
- Step-by-step execution tracking
- Human-in-the-loop safety checks
- Unique run IDs and timestamps
- Execution history API
- Automated tests and input validation

## How It Works

1. **User Input:** The user enters a goal in natural language.
2. **Planning:** The planner identifies the task category and creates ordered steps.
3. **Execution:** Safe internal demonstration steps are simulated.
4. **Safety:** Sensitive actions are flagged for human approval.
5. **Monitoring:** Execution logs and run details are returned.

## Technology Stack

- Python
- FastAPI
- Pydantic
- HTML, CSS and JavaScript
- Pytest
- Vercel

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application interface |
| POST | `/api/run` | Create and execute a demo workflow |
| GET | `/api/history` | View workflow history |
| GET | `/health` | Health check |

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

## Run Tests

```bash
pytest -v
```

## Safety and Limitations

AgentFlow AI currently demonstrates workflow planning and simulated execution. It does not perform real external actions such as sending emails, deleting files or making payments.

Sensitive actions are identified and flagged for human approval.

## Future Scope

- LLM-based dynamic planning
- Tool and API integrations
- Persistent workflow storage
- Interactive approval controls
- Real-time execution monitoring

## Deployment

Live Demo: https://prompt-wars-x-agent-x-2-0-nu.vercel.app

GitHub: https://github.com/mayanksingh232005-alt/PromptWars-x-Agent-X-2.0
