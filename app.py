from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone
import uuid

app = FastAPI(title="AgentFlow AI", version="1.0.0")

runs = []

class GoalRequest(BaseModel):
    goal: str

def plan_goal(goal: str):
    """Create a transparent, explainable workflow plan from a user's goal."""
    g = goal.strip()
    lower = g.lower()
    if not g:
        return []
    if any(k in lower for k in ["research", "compare", "find", "analyze"]):
        tasks = [
            ("Understand the request", "Extract the objective, constraints, and expected output."),
            ("Break down the work", "Create focused research and analysis subtasks."),
            ("Prepare findings", "Organize evidence and produce a concise result."),
            ("Quality check", "Check completeness, consistency, and missing information.")
        ]
    elif any(k in lower for k in ["email", "message", "reply", "draft"]):
        tasks = [
            ("Understand communication goal", "Identify recipient, purpose, and tone."),
            ("Draft content", "Prepare a message matching the requested goal."),
            ("Review content", "Check clarity, tone, and completeness."),
            ("Request approval", "Require user review before any message is sent.")
        ]
    elif any(k in lower for k in ["report", "document", "summary", "write"]):
        tasks = [
            ("Define deliverable", "Identify audience, format, and key points."),
            ("Create outline", "Arrange the content into logical sections."),
            ("Generate first draft", "Produce the requested content."),
            ("Validate output", "Check structure, accuracy, and completeness.")
        ]
    else:
        tasks = [
            ("Interpret objective", "Convert the goal into clear success criteria."),
            ("Plan workflow", "Split the objective into small, ordered tasks."),
            ("Execute safe steps", "Complete steps that do not require external permissions."),
            ("Review result", "Check the result against the original objective.")
        ]
    return [{"id": i+1, "title": title, "description": desc,
             "status": "planned"} for i, (title, desc) in enumerate(tasks)]

def execute_plan(goal: str, plan):
    """Demo executor: simulates safe internal workflow steps; no external side effects."""
    output = []
    for task in plan:
        task["status"] = "completed"
        output.append(f"{task['title']}: {task['description']}")
    return {
        "summary": f"Created and completed a safe demo workflow for: {goal}",
        "steps": output,
        "approval_required": any(k in goal.lower() for k in ["send", "delete", "purchase", "pay", "publish"])
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AgentFlow AI</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#0b1020;color:#edf2ff;font:16px Arial,sans-serif}
.wrap{max-width:980px;margin:48px auto;padding:20px}.tag{color:#9caeff;font-weight:bold;letter-spacing:2px}
h1{font-size:42px;margin:12px 0}p{color:#b9c3dc;line-height:1.6}
.panel{background:#141d33;border:1px solid #293756;border-radius:18px;padding:24px;margin-top:24px}
textarea{width:100%;min-height:120px;background:#0b1326;color:white;border:1px solid #3b4b70;border-radius:10px;padding:14px;font-size:16px}
button{background:#748cff;color:#081024;border:0;border-radius:10px;padding:13px 20px;font-weight:bold;cursor:pointer;margin-top:12px}
.card{background:#0e172b;border:1px solid #293756;border-radius:12px;padding:16px;margin:12px 0}
.small{font-size:13px;color:#98a8c8}.pill{display:inline-block;padding:6px 10px;border-radius:20px;background:#20345c;color:#b9caff;font-size:12px}
#result{white-space:pre-wrap;line-height:1.7;color:#d9e2ff}
</style></head><body><div class="wrap">
<div class="tag">PS01 · AGENTIC WORKFLOW AUTOMATION</div><h1>AgentFlow AI</h1>
<p>Turn a goal into an explainable workflow. The planner breaks work into steps, the executor completes safe demo actions, and sensitive actions are flagged for human approval.</p>
<div class="panel"><span class="pill">AI workflow planner</span> <span class="pill">Human-in-the-loop</span> <span class="pill">Audit-friendly</span>
<h2>What do you want to get done?</h2>
<textarea id="goal" placeholder="Example: Research three project management tools and prepare a comparison report."></textarea>
<button onclick="run()">Generate & run workflow</button>
<div id="result" style="margin-top:20px"></div></div>
<div class="panel"><h2>How it works</h2>
<div class="card"><b>1. Planner</b><p>Understands the goal and creates ordered tasks.</p></div>
<div class="card"><b>2. Executor</b><p>Runs safe internal demo steps and tracks status.</p></div>
<div class="card"><b>3. Human approval</b><p>Flags actions like sending, deleting, purchasing, or publishing for explicit approval.</p></div>
<div class="card"><b>4. Quality review</b><p>Checks whether the workflow steps address the original goal.</p></div>
</div></div>
<script>
async function run(){
 const goal=document.getElementById('goal').value.trim(), out=document.getElementById('result');
 if(!goal){out.textContent='Please enter a goal first.';return}
 out.textContent='Planning and executing...';
 try{
  const r=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({goal})});
  const d=await r.json();
  out.textContent='WORKFLOW PLAN\\n'+d.plan.map(x=>`${x.id}. ${x.title} — ${x.status}\\n   ${x.description}`).join('\\n')+
   '\\n\\nRESULT\\n'+d.result.summary+
   (d.result.approval_required?'\\n\\nHUMAN APPROVAL REQUIRED: This goal may involve an external or sensitive action. No such action was performed.':'')+
   '\\n\\nRun ID: '+d.run_id;
 }catch(e){out.textContent='Could not run workflow: '+e}
}
</script></body></html>
"""

@app.post("/api/run")
def run_workflow(req: GoalRequest):
    goal = req.goal.strip()
    if not goal:
        return {"error": "Goal cannot be empty"}
    plan = plan_goal(goal)
    result = execute_plan(goal, plan)
    run = {
        "run_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "plan": plan,
        "result": result
    }
    runs.append(run)
    return run

@app.get("/health")
def health():
    return {"status": "ok"}
