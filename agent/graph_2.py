
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
import json
import re

from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files
from config import GROQ_MODEL

_ = load_dotenv()
groq_key = os.getenv(GROQ_API_KEY)

llm = ChatGroq(model=GROQ_MODEL, temperature=0,
api_key = )


def safe_json_parse(text: str, max_attempts=3) -> dict:
   
    
    # Strategy 1: Direct parse
    try:
        return json.loads(text)
    except:
        pass
    
    # Strategy 2: Extract from code blocks
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            pass
    
    
    match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
    if match:
        json_str = match.group(0)
        
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)  # Remove trailing commas
        json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_str)  # Remove control chars
        
        try:
            return json.loads(json_str)
        except:
            pass
    
    
    try:
        # Look for simple patterns
        name_match = re.search(r'"name"\s*:\s*"([^"]+)"', text)
        desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', text)
        tech_match = re.search(r'"techstack"\s*:\s*"([^"]+)"', text)
        
        if name_match and desc_match and tech_match:
            return {
                "name": name_match.group(1),
                "description": desc_match.group(1),
                "techstack": tech_match.group(1),
                "features": ["basic functionality"],
                "files": [
                    {"path": "index.html", "purpose": "main file"},
                    {"path": "style.css", "purpose": "styling"},
                    {"path": "script.js", "purpose": "logic"}
                ]
            }
    except:
        pass
    
    raise ValueError(f"Could not parse JSON from response. Text: {text[:200]}...")


def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    
    
    prompt = f"""Create a simple project plan for: {user_prompt}

Return ONLY this JSON (no other text):
{{
  "name": "ProjectName",
  "description": "One line description",
  "techstack": "HTML, CSS, JavaScript",
  "features": ["feature 1", "feature 2"],
  "files": [
    {{"path": "index.html", "purpose": "main page"}},
    {{"path": "style.css", "purpose": "styles"}},
    {{"path": "script.js", "purpose": "code"}}
  ]
}}"""
    
    for attempt in range(3):
        try:
            response = llm.invoke(prompt)
            response_text = response.content.strip()
            
            print(f"\n=== PLANNER ATTEMPT {attempt + 1} ===")
            print(response_text[:300])
            
            plan_dict = safe_json_parse(response_text)
            plan = Plan(**plan_dict)
            print(f"✓ Successfully parsed plan: {plan.name}")
            return {"plan": plan}
            
        except Exception as e:
            print(f"✗ Attempt {attempt + 1} failed: {e}")
            if attempt == 2:
                # Last attempt - create a default plan
                print("Creating default plan...")
                plan = Plan(
                    name="Simple Project",
                    description=user_prompt[:100],
                    techstack="HTML, CSS, JavaScript",
                    features=["basic functionality"],
                    files=[
                        File(path="index.html", purpose="main HTML file"),
                        File(path="style.css", purpose="CSS styling"),
                        File(path="script.js", purpose="JavaScript code")
                    ]
                )
                return {"plan": plan}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    
    # Create simple tasks directly without AI
    print("\n=== ARCHITECT: Creating tasks ===")
    
    tasks = []
    for file in plan.files:
        task = ImplementationTask(
            filepath=file.path,
            task_description=f"Create {file.path}: {file.purpose}. "
            f"Implement for project '{plan.name}' using {plan.techstack}. "
            f"Features: {', '.join(plan.features[:3])}."
        )
        tasks.append(task)
        print(f"✓ Task created for {file.path}")
    
    task_plan = TaskPlan(implementation_steps=tasks)
    task_plan.plan = plan
    
    return {"task_plan": task_plan}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    existing_content = read_file.run(current_task.filepath)

    print(f"\n=== CODER: Working on {current_task.filepath} ===")

    system_prompt = """You are a code generator. 
Write complete, working code files.
Use write_file(path, content) to save your code.
Make the code functional and well-structured."""

    user_prompt = (
        f"Create this file: {current_task.filepath}\n"
        f"Task: {current_task.task_description}\n\n"
        f"Existing content: {existing_content if existing_content else 'None - create new file'}\n\n"
        "Write the complete file content using write_file(path, content)."
    )

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)

    try:
        react_agent.invoke({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        })
        print(f"✓ Completed {current_task.filepath}")
    except Exception as e:
        print(f"✗ Error on {current_task.filepath}: {e}")

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}


graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")
agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke(
        {"user_prompt": "Build a simple calculator in HTML CSS and JavaScript"},
        {"recursion_limit": 100}
    )
    print("\n=== FINAL STATE ===")
    print("Generation complete!")
