# 🎯 LangGraph Tutorial - Step by Step

**Start here if you're completely new to LangGraph!**

---

## 🎓 Lesson 1: Understanding State

The **state** is like a piece of paper that gets passed between people.

```python
# state.py - Open this file and read it

class AgentState(TypedDict):
    messages: List[str]    # What the user wants
    action: str            # What we'll do
    username: str          # Who we'll do it to
    extra_info: str        # Extra details
    result: str            # What happened
    next_step: str         # Where to go next
```

**🧪 Try it:**
Open `state.py` and look at the example at the bottom. See how state changes as it flows through agents!

---

## 🎓 Lesson 2: Creating an Agent (Node)

An **agent** is just a function that:
1. Takes state as input
2. Does some work
3. Updates state
4. Returns state

```python
# agents.py - Look at role_agent

def role_agent(state: AgentState) -> AgentState:
    # Read from state
    username = state["username"]
    role = state["extra_info"]
    
    # Do work (in this case, simulated)
    print(f"Assigning {role} to {username}")
    
    # Update state
    state["result"] = f"✓ Success!"
    state["next_step"] = "end"
    
    # Return state
    return state
```

**🧪 Try it:**
```bash
python agents.py
```
This runs each agent separately so you can see how they work!

---

## 🎓 Lesson 3: The Supervisor

The **supervisor** uses AI (GPT) to understand what the user wants.

```python
# supervisor.py - Look at supervisor_agent

def supervisor_agent(state: AgentState) -> AgentState:
    # 1. Get user message
    user_message = state["messages"][0]
    
    # 2. Ask GPT to analyze it
    llm = ChatOpenAI(model="gpt-4o-mini")
    response = llm.invoke(prompt)
    
    # 3. Parse GPT's response
    state["action"] = "assign_role"
    state["username"] = "john.doe"
    
    # 4. Decide where to route
    state["next_step"] = "role_agent"
    
    return state
```

**🧪 Try it:**
```bash
python supervisor.py
```
This tests the supervisor in isolation!

---

## 🎓 Lesson 4: Building the Workflow

This is where **LangGraph magic** happens!

```python
# workflow.py - Study this carefully!

# Step 1: Create the graph
workflow = StateGraph(AgentState)

# Step 2: Add nodes (agents)
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("role_agent", role_agent)

# Step 3: Set starting point
workflow.set_entry_point("supervisor")

# Step 4: Add edges (connections)
workflow.add_conditional_edges(
    "supervisor",           # From this node
    route_to_next,          # Use this function to decide
    {                       # Possible destinations
        "role_agent": "role_agent",
        END: END
    }
)

# Step 5: Compile
app = workflow.compile()

# Step 6: Run it!
result = app.invoke(initial_state)
```

**🧪 Try it:**
```bash
python workflow.py
```
This runs the complete workflow!

---

## 🎓 Lesson 5: Understanding Routing

**Routing** decides which agent runs next.

```python
def route_to_next(state: AgentState) -> str:
    # Read state
    next_step = state["next_step"]
    
    # Make decision
    if next_step == "end":
        return END  # Stop!
    else:
        return next_step  # Go to that agent
```

**Key Points:**
- Routing functions read `state`
- They return the name of the next node
- Or return `END` to stop

---

## 🎓 Lesson 6: Two Types of Edges

### Fixed Edge (Simple)
```python
# Always go from A to B
workflow.add_edge("A", "B")
```

### Conditional Edge (Smart)
```python
# Decide where to go based on state
workflow.add_conditional_edges(
    "supervisor",
    route_to_next,  # Decision function
    {
        "agent1": "agent1",
        "agent2": "agent2",
        END: END
    }
)
```

---

## 🎓 Lesson 7: The Complete Flow

Let's trace what happens when you run the system:

```
1. User types: "Assign HR Manager to john.doe"

2. Initial state created:
   {
       messages: ["Assign HR Manager to john.doe"],
       next_step: "supervisor"
   }

3. Workflow starts at "supervisor" (entry point)

4. Supervisor agent:
   - Reads message
   - Uses GPT to understand it
   - Sets: action="assign_role", username="john.doe"
   - Sets: next_step="role_agent"

5. Router looks at next_step, goes to "role_agent"

6. Role agent:
   - Does the work (simulated)
   - Sets: result="✓ Success!"
   - Sets: next_step="end"

7. Router sees "end", stops

8. Final state returned to user!
```

---

## 🎓 Lesson 8: Running the Full App

```bash
python main.py
```

**Try these:**
1. `Assign HR Manager role to john.doe`
2. `Reset password for jane.smith`
3. `Unlock user bob.jones`

**Watch what happens:**
- See the supervisor analyze your request
- See which agent it routes to
- See the agent do the work
- See the final result!

---

## 🎓 Lesson 9: Experiment!

Now that you understand the basics, try modifying things:

### Easy Experiments:
1. **Change the simulated responses** in `agents.py`
2. **Add print statements** to see state at each step
3. **Change the prompt** in `supervisor.py`

### Medium Experiments:
1. **Add a new agent** - Create `def new_agent(state)` in `agents.py`
2. **Add new agent to workflow** in `workflow.py`
3. **Update supervisor** to route to your new agent

### Advanced Experiments:
1. **Add conversation history** - Keep track of previous messages
2. **Add validation** - Check if username exists before proceeding
3. **Add error handling** - What if the API fails?

---

## 🎓 Lesson 10: Key Takeaways

### What is LangGraph?
- A framework for building **multi-agent** systems
- Uses a **state** that flows between agents
- Provides **visual workflow** representation

### Core Concepts:
1. **State** - Shared data structure
2. **Nodes** - Agents (functions that process state)
3. **Edges** - Connections between agents
4. **Routing** - Logic to decide which agent runs next
5. **Workflow** - The complete system

### Why LangGraph?
- Easy to understand and visualize
- Built-in state management
- Flexible routing
- Great for complex agent systems

---

## 🎯 Practice Exercises

### Exercise 1: Add a New Field to State
Add `timestamp` to track when requests are made.

### Exercise 2: Create a Validation Agent
Add an agent that validates the username exists before doing work.

### Exercise 3: Add Logging
Make each agent log what it's doing to a file.

### Exercise 4: Add Error Handling
What happens if the supervisor can't understand the request?

### Exercise 5: Multi-turn Conversations
Allow the user to have a back-and-forth conversation.

---

## 📚 Next Steps

Once you're comfortable with this:

1. ✅ Read the official LangGraph docs
2. ✅ Try the complex version with real database
3. ✅ Build your own agent system
4. ✅ Explore advanced LangGraph features:
   - Subgraphs
   - Persistence
   - Human-in-the-loop
   - Streaming

---

## 🎉 Congratulations!

You now understand the fundamentals of LangGraph!

**Remember:**
- State flows through agents
- Agents read, process, and update state
- Workflows connect agents together
- Routing decides the path

**Keep building and experimenting!** 🚀