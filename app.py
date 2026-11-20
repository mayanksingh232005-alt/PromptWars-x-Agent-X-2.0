
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List
import uuid

app = FastAPI(
    title="AgentFlow AI",
    description="Agentic Workflow Automation with Human Approval",
    version="2.0.0"
)

runs = []
MAX_RUNS = 100

SENSITIVE_KEYWORDS = [
    "send", "delete", "purchase", "pay", "payment",
    "publish", "transfer", "submit", "book"
]


class GoalRequest(BaseModel):
    goal: str = Field(min_length=3, max_length=1000)


def plan_goal(goal: str):
    """Convert a user goal into an explainable workflow."""

    text = goal.strip().lower()

    if any(word in text for word in ["research", "compare", "find", "analyze"]):
        tasks = [
            ("Understand the request",
             "Identify objectives, constraints and expected output."),
            ("Break down the work",
             "Create focused research and analysis subtasks."),
            ("Prepare findings",
             "Organize information into a structured result."),
            ("Quality check",
             "Review completeness, consistency and missing information.")
        ]

    elif any(word in text for word in ["email", "message", "reply", "draft"]):
        tasks = [
            ("Understand communication goal",
             "Identify recipient, purpose and tone."),
            ("Prepare draft",
             "Create content according to the requested objective."),
            ("Review message",
             "Check clarity, tone and completeness."),
            ("Approval checkpoint",
             "Ask the user to review before any external communication.")
        ]

    elif any(word in text for word in ["report", "document", "summary", "write"]):
        tasks = [
            ("Define deliverable",
             "Identify audience, format and key requirements."),
            ("Create outline",
             "Organize the content into logical sections."),
            ("Prepare first draft",
             "Generate a structured draft."),
            ("Validate output",
             "Review structure, accuracy and completeness.")
        ]

    else:
        tasks = [
            ("Interpret objective",
             "Convert the goal into clear success criteria."),
            ("Plan workflow",
             "Divide the objective into ordered tasks."),
            ("Execute safe steps",
             "Process safe internal demonstration tasks."),
            ("Review result",
             "Check the result against the original objective.")
        ]

    return [
        {
            "id": index + 1,
            "title": title,
            "description": description,
            "status": "planned"
        }
        for index, (title, description) in enumerate(tasks)
    ]


def execute_plan(goal: str, plan: list):
    """Simulate safe internal execution. No external action is performed."""

    approval_required = any(
        keyword in goal.lower()
        for keyword in SENSITIVE_KEYWORDS
    )

    execution_log = []

    for task in plan:
        if approval_required and task["title"] == "Approval checkpoint":
            task["status"] = "awaiting_approval"
        else:
            task["status"] = "completed"

        execution_log.append({
            "step": task["title"],
            "status": task["status"],
            "message": task["description"]
        })

    return {
        "summary": (
            "Workflow prepared successfully. "
            "Sensitive external actions are not performed automatically."
        ),
        "approval_required": approval_required,
        "execution_log": execution_log,
        "safety_note": (
            "User approval is required before sensitive actions."
            if approval_required
            else "Only safe internal demo steps were simulated."
        )
    }


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AgentFlow AI</title>
<style>
*{box-sizing:border-box}
body{
 margin:0;background:#0b1020;color:#edf2ff;
 font:16px Arial,sans-serif
}
.wrap{max-width:980px;margin:40px auto;padding:20px}
.tag{color:#9caeff;font-weight:bold;letter-spacing:2px}
h1{font-size:42px;margin:12px 0}
p{color:#b9c3dc;line-height:1.6}
.panel{
 background:#141d33;border:1px solid #293756;
 border-radius:18px;padding:24px;margin-top:24px
}
textarea{
 width:100%;min-height:120px;background:#0b1326;
 color:white;border:1px solid #3b4b70;
 border-radius:10px;padding:14px;font-size:16px
}
button{
 background:#748cff;color:#081024;border:0;
 border-radius:10px;padding:13px 20px;
 font-weight:bold;cursor:pointer;margin-top:12px
}
button:disabled{opacity:.6;cursor:wait}
.card{
 background:#0e172b;border:1px solid #293756;
 border-radius:12px;padding:16px;margin:12px 0
}
.pill{
 display:inline-block;padding:6px 10px;
 border-radius:20px;background:#20345c;
 color:#b9caff;font-size:12px;margin-right:5px
}
.small{font-size:13px;color:#98a8c8}
#result{margin-top:20px;line-height:1.7}
.step{border-left:3px solid #748cff;padding:10px 14px;margin:12px 0}
.status{color:#9caeff;font-size:13px}
.error{color:#ff9b9b}
</style>
</head>
<body>
<div class="wrap">
<div class="tag">PS01 · AGENTIC WORKFLOW AUTOMATION</div>
<h1>AgentFlow AI</h1>
<p>
Turn natural-language goals into structured workflows.
Plan tasks, track execution and keep sensitive actions
under human supervision.
</p>

<div class="panel">
<span class="pill">AI Workflow Planner</span>
<span class="pill">Human-in-the-loop</span>
<span class="pill">Execution Tracking</span>

<h2>What do you want to get done?</h2>
<textarea id="goal" maxlength="1000"
placeholder="Example: Research three AI project management tools and prepare a comparison report."></textarea>
<button id="runButton" onclick="runWorkflow()">
Generate & Run Workflow
</button>
<div id="result"></div>
</div>

<div class="panel">
<h2>How it works</h2>
<div class="card">
<b>1. Planner</b>
<p>Understands the goal and creates ordered tasks.</p>
</div>
<div class="card">
<b>2. Executor</b>
<p>Simulates safe internal workflow steps.</p>
</div>
<div class="card">
<b>3. Human Approval</b>
<p>Flags sensitive actions for explicit user approval.</p>
</div>
<div class="card">
<b>4. Quality Review</b>
<p>Checks the workflow against the original objective.</p>
</div>
</div>

<div class="panel">
<h2>Safety and Transparency</h2>
<p>
AgentFlow AI is a demonstration system. It does not
automatically send messages, delete data, make payments
or perform external actions.
</p>
</div>
</div>

<script>
async function runWorkflow(){
 const goal=document.getElementById("goal").value.trim();
 const result=document.getElementById("result");
 const button=document.getElementById("runButton");

 if(goal.length<3){
   result.innerHTML='<p class="error">Please enter a goal with at least 3 characters.</p>';
   return;
 }

 button.disabled=true;
 result.textContent="Planning and executing workflow...";

 try{
   const response=await fetch("/api/run",{
     method:"POST",
     headers:{"Content-Type":"application/json"},
     body:JSON.stringify({goal:goal})
   });

   const data=await response.json();

   if(!response.ok){
     throw new Error(data.detail || "Workflow request failed.");
   }

   let html="<h2>Workflow Plan</h2>";

   data.plan.forEach(task=>{
     html+=`
       <div class="step">
         <b>${task.id}. ${escapeHTML(task.title)}</b>
         <div>${escapeHTML(task.description)}</div>
         <div class="status">Status: ${escapeHTML(task.status)}</div>
       </div>`;
   });

   html+="<h2>Result</h2>";
   html+=`<p>${escapeHTML(data.result.summary)}</p>`;

   if(data.result.approval_required){
     html+='<p class="error"><b>Human approval required:</b> No external action was performed.</p>';
   }

   html+=`<p class="small">${escapeHTML(data.result.safety_note)}</p>`;
   html+=`<p class="small">Run ID: ${escapeHTML(data.run_id)}</p>`;
   html+=`<p class="small">Created: ${escapeHTML(data.created_at)}</p>`;

   html+="<h3>Execution Log</h3>";

   data.result.execution_log.forEach(item=>{
     html+=`<div class="card">
       <b>${escapeHTML(item.step)}</b>
       <div class="status">${escapeHTML(item.status)}</div>
       <p>${escapeHTML(item.message)}</p>
     </div>`;
   });

   result.innerHTML=html;

 }catch(error){
   result.innerHTML='<p class="error">'+escapeHTML(error.message)+'</p>';
 }finally{
   button.disabled=false;
 }
}

function escapeHTML(value){
 return String(value).replace(/[&<>"']/g,function(char){
   return {
     "&":"&amp;",
     "<":"&lt;",
     ">":"&gt;",
     '"':"&quot;",
     "'":"&#39;"
   }[char];
 });
}
</script>
</body>
</html>
"""


@app.post("/api/run")
def run_workflow(request: GoalRequest):
    goal = request.goal.strip()

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

    if len(runs) > MAX_RUNS:
        runs.pop(0)

    return run


@app.get("/api/history")
def get_history():
    return {
        "total_runs": len(runs),
        "runs": runs
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "AgentFlow AI",
        "version": "2.0.0"
    }
