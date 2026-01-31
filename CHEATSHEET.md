# 🎯 LangGraph Quick Reference - Cheat Sheet

## 📋 Setup (Copy-Paste Ready)

```bash
# Install
pip install langgraph langchain langchain-openai python-dotenv

# Create .env
echo "OPENAI_API_KEY=your_key_here" > .env

# Run
python main.py
```

---

## 🧱 Basic Structure

### 1. Define State
```python
from typing import TypedDict

class AgentState(TypedDict):
    messages: list[str]    # User input
    result: str            # Output
    next_step: str         # Where to go next
```

### 2. Create Agent (Node)
```python
def my_agent(state: AgentState) -> AgentState:
    # Read state
    user_input = state["messages"][0]
    
    # Do work
    result = process(user_input)
    
    # Update state
    state["result"] = result
    state["next_step"] = "end"
    
    # Return state
    return state
```

### 3. Build Workflow
```python
from langgraph.graph import StateGraph, END

# Create graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent1", agent1_function)
workflow.add_node("agent2", agent2_function)

# Set start
workflow.set_entry_point("agent1")

# Add edges
workflow.add_edge("agent1", "agent2")  # Fixed
workflow.add_edge("agent2", END)       # To end

# Compile
app = workflow.compile()
```

### 4. Run It
```python
# Create initial state
initial_state = AgentState(
    messages=["Hello"],
    result="",
    next_step="agent1"
)

# Run workflow
final_state = app.invoke(initial_state)

# Get result
print(final_state["result"])
```

---

## 🔀 Routing (Conditional Edges)

```python
# Define routing function
def route_to_next(state: AgentState) -> str:
    if state["next_step"] == "end":
        return END
    return state["next_step"]

# Add conditional edge
workflow.add_conditional_edges(
    "supervisor",      # From this node
    route_to_next,     # Decision function
    {
        "agent1": "agent1",
        "agent2": "agent2",
        END: END
    }
)
```

---

## 🎯 Common Patterns

### Supervisor Pattern
```python
def supervisor(state: AgentState) -> AgentState:
    user_input = state["messages"][0]
    
    # Use LLM to decide
    if "role" in user_input:
        state["next_step"] = "role_agent"
    elif "password" in user_input:
        state["next_step"] = "password_agent"
    else:
        state["next_step"] = "end"
    
    return state
```

### Sequential Pattern
```python
workflow.add_node("step1", step1)
workflow.add_node("step2", step2)
workflow.add_node("step3", step3)

workflow.set_entry_point("step1")
workflow.add_edge("step1", "step2")
workflow.add_edge("step2", "step3")
workflow.add_edge("step3", END)
```

### Parallel-then-Merge Pattern
```python
workflow.add_node("start", start)
workflow.add_node("worker1", worker1)
workflow.add_node("worker2", worker2)
workflow.add_node("merge", merge)

workflow.set_entry_point("start")
workflow.add_edge("start", "worker1")
workflow.add_edge("start", "worker2")
workflow.add_edge("worker1", "merge")
workflow.add_edge("worker2", "merge")
workflow.add_edge("merge", END)
```

---

## 🔧 Using LLMs in Agents

```python
from langchain_openai import ChatOpenAI

def agent_with_llm(state: AgentState) -> AgentState:
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Create prompt
    prompt = f"Analyze this: {state['messages'][0]}"
    
    # Get response
    response = llm.invoke(prompt)
    
    # Update state
    state["result"] = response.content
    state["next_step"] = "end"
    
    return state
```

---

## 📊 State Management Tips

### ✅ Good Practice
```python
# Clear field names
state["username"] = "john.doe"
state["action"] = "assign_role"

# Use next_step for routing
state["next_step"] = "next_agent"

# Store results
state["result"] = "Success!"
```

### ❌ Avoid
```python
# Don't use vague names
state["data"] = something

# Don't mutate without returning
def bad_agent(state):
    state["x"] = 1
    # Missing return!

# Don't forget next_step
state["next_step"] = ""  # No routing info!
```

---

## 🐛 Debugging Tips

### Add Print Statements
```python
def my_agent(state: AgentState) -> AgentState:
    print(f"🔍 Agent received: {state}")
    # ... do work ...
    print(f"✅ Agent returning: {state}")
    return state
```

### Test Agents Individually
```python
# Test one agent at a time
test_state = AgentState(messages=["test"], ...)
result = my_agent(test_state)
print(result)
```

### Check State at Each Step
```python
# In your main code
states = []
for step_output in app.stream(initial_state):
    states.append(step_output)
    print(f"After step: {step_output}")
```

---

## 🎯 Common Mistakes

### 1. Forgetting to Return State
```python
# ❌ Wrong
def bad_agent(state):
    state["result"] = "done"
    # No return!

# ✅ Correct
def good_agent(state):
    state["result"] = "done"
    return state
```

### 2. Not Setting next_step
```python
# ❌ Wrong
def bad_agent(state):
    state["result"] = "done"
    # next_step not set!
    return state

# ✅ Correct
def good_agent(state):
    state["result"] = "done"
    state["next_step"] = "end"
    return state
```

### 3. Wrong Edge Configuration
```python
# ❌ Wrong - node name doesn't exist
workflow.add_edge("agent1", "non_existent")

# ✅ Correct
workflow.add_node("agent2", agent2)
workflow.add_edge("agent1", "agent2")
```

---

## 📚 Complete Minimal Example

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. Define state
class State(TypedDict):
    message: str
    result: str
    next_step: str

# 2. Create agents
def agent1(state: State) -> State:
    state["result"] = f"Agent1 processed: {state['message']}"
    state["next_step"] = "agent2"
    return state

def agent2(state: State) -> State:
    state["result"] += " -> Agent2 done!"
    state["next_step"] = "end"
    return state

# 3. Build workflow
workflow = StateGraph(State)
workflow.add_node("agent1", agent1)
workflow.add_node("agent2", agent2)
workflow.set_entry_point("agent1")
workflow.add_edge("agent1", "agent2")
workflow.add_edge("agent2", END)
app = workflow.compile()

# 4. Run
result = app.invoke({
    "message": "Hello",
    "result": "",
    "next_step": "agent1"
})

print(result["result"])
# Output: Agent1 processed: Hello -> Agent2 done!
```

---

## 🚀 Quick Commands

```bash
# Run main app
python main.py

# Test individual components
python state.py       # Understand state
python supervisor.py  # Test supervisor
python agents.py      # Test agents
python workflow.py    # Test workflow

# Install specific version
pip install langgraph==0.2.45
```

---

## 📖 Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Examples](https://github.com/langchain-ai/langgraph/tree/main/examples)
- [Discord](https://discord.gg/langchain)

---

**Keep this handy while coding!** 📌