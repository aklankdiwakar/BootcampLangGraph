# 🎓 Simple Fusion HCM Agent - LangGraph Learning Project

**A beginner-friendly introduction to LangGraph!**

No complex databases, no encryption, just the core concepts you need to understand.

---

## 📚 What You'll Learn

1. **LangGraph State** - How state flows through agents
2. **Nodes** - Individual agents that do work
3. **Edges** - Connections between agents
4. **Routing** - How to decide which agent runs next
5. **Workflows** - Putting it all together

---

## 🗂️ Project Structure (Only 6 Files!)

```
simple_fusion_agent/
├── state.py          ← The shared state (most important!)
├── supervisor.py     ← The "brain" that decides what to do
├── agents.py         ← Three simple worker agents
├── workflow.py       ← Connects everything with LangGraph
├── main.py           ← Run this to try it out!
└── requirements.txt  ← Dependencies
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install

```bash
cd simple_fusion_agent
pip install -r requirements.txt
```

### Step 2: Configure

Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 3: Run!

```bash
python main.py
```

Try these commands:
- `Assign HR Manager role to john.doe`
- `Reset password for jane.smith`
- `Unlock user bob.jones`

---

## 🧠 Understanding the Code

### 1️⃣ State (`state.py`)

**The most important concept in LangGraph!**

Think of state as a **shared notebook** that gets passed between agents. Each agent can:
- Read information from it
- Add/update information
- Decide where to go next

```python
class AgentState(TypedDict):
    messages: List[str]     # What the user said
    action: str             # What to do
    username: str           # Who to do it to
    extra_info: str         # Additional details
    result: str             # The final result
    next_step: str          # Where to go next
```

**Example Flow:**
```
User input: "Assign HR Manager to john.doe"

State after Supervisor:
{
    "messages": ["Assign HR Manager to john.doe"],
    "action": "assign_role",
    "username": "john.doe",
    "extra_info": "HR Manager",
    "next_step": "role_agent"  ← Routes to role agent
}

State after Role Agent:
{
    ... (same as above)
    "result": "✓ Successfully assigned HR Manager to john.doe",
    "next_step": "end"  ← We're done!
}
```

---

### 2️⃣ Supervisor (`supervisor.py`)

**The decision maker.**

Uses GPT to understand the user's request and decides:
- What action? (assign_role, reset_password, unlock_user)
- Which username?
- What extra info? (like role name)

```python
def supervisor_agent(state: AgentState) -> AgentState:
    # 1. Read user's message
    user_message = state["messages"][0]
    
    # 2. Ask GPT to analyze it
    response = llm.invoke(prompt)
    
    # 3. Update state with the decision
    state["action"] = "assign_role"
    state["username"] = "john.doe"
    state["next_step"] = "role_agent"
    
    return state
```

---

### 3️⃣ Agents (`agents.py`)

**The workers.**

Three simple agents that do the actual work:

```python
def role_agent(state: AgentState) -> AgentState:
    # Simulate assigning a role
    state["result"] = f"✓ Assigned {state['extra_info']} to {state['username']}"
    state["next_step"] = "end"
    return state

def password_agent(state: AgentState) -> AgentState:
    # Simulate resetting password
    new_password = generate_random_password()
    state["result"] = f"✓ New password: {new_password}"
    state["next_step"] = "end"
    return state

def unlock_agent(state: AgentState) -> AgentState:
    # Simulate unlocking user
    state["result"] = f"✓ Unlocked {state['username']}"
    state["next_step"] = "end"
    return state
```

---

### 4️⃣ Workflow (`workflow.py`)

**The magic happens here!**

This is where we use LangGraph to connect everything:

```python
# 1. Create the graph
workflow = StateGraph(AgentState)

# 2. Add nodes (agents)
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("role_agent", role_agent)
workflow.add_node("password_agent", password_agent)
workflow.add_node("unlock_agent", unlock_agent)

# 3. Set starting point
workflow.set_entry_point("supervisor")

# 4. Add routing logic
workflow.add_conditional_edges(
    "supervisor",
    route_to_next,  # Function that decides where to go
    {
        "role_agent": "role_agent",
        "password_agent": "password_agent",
        "unlock_agent": "unlock_agent",
        END: END
    }
)

# 5. Compile and run!
app = workflow.compile()
result = app.invoke(initial_state)
```

---

## 📊 Visual Workflow

```
          START
            ↓
      [Supervisor]  ← Uses GPT to understand request
            ↓
       (Decision)
      /    |    \
     /     |     \
  [Role][Pass][Unlock]  ← Do the work
     \     |     /
      \    |    /
          END
```

---

## 🎯 Key LangGraph Concepts

### Nodes
- Functions that process state
- Each node is an agent
- `workflow.add_node("name", function)`

### Edges
- Connections between nodes
- Fixed: Always go to the same place
- Conditional: Decide based on state

### Routing
- How to decide which node to visit next
- Read `state["next_step"]` 
- Return the name of the next node or `END`

### State
- Shared data structure
- Gets passed to every node
- Nodes can read and modify it

---

## 🧪 Testing Individual Components

Each file can be run standalone for testing:

```bash
# Test the state concept
python state.py

# Test the supervisor
python supervisor.py

# Test the agents
python agents.py

# Test the workflow
python workflow.py

# Run the full interactive demo
python main.py
```

---

## 🔍 Understanding the Flow

Let's trace a request through the system:

**Input:** "Assign HR Manager role to john.doe"

1. **Main** creates initial state:
   ```python
   {
       "messages": ["Assign HR Manager role to john.doe"],
       "next_step": "supervisor"
   }
   ```

2. **Supervisor** analyzes with GPT:
   ```python
   state["action"] = "assign_role"
   state["username"] = "john.doe"
   state["extra_info"] = "HR Manager"
   state["next_step"] = "role_agent"
   ```

3. **Router** sees `next_step = "role_agent"`, routes there

4. **Role Agent** does the work:
   ```python
   state["result"] = "✓ Successfully assigned HR Manager to john.doe"
   state["next_step"] = "end"
   ```

5. **Router** sees `next_step = "end"`, stops

6. **Main** displays the result!

---

## 🎓 Next Steps for Learning

Once you understand this simple version:

1. **Add a real database** - Replace simulated data with actual storage
2. **Add real API calls** - Call actual Fusion HCM endpoints
3. **Add encryption** - Secure credential storage
4. **Add error handling** - Handle failures gracefully
5. **Add conversation history** - Make it remember past interactions
6. **Add more agents** - Expand functionality

---

## 💡 Pro Tips

1. **Start with state.py** - Understand the state structure first
2. **Run each file separately** - Test components individually
3. **Add print statements** - See what's happening at each step
4. **Draw the workflow** - Sketch it on paper to visualize
5. **Experiment!** - Change things and see what happens

---

## ❓ Common Questions

**Q: Why LangGraph instead of just chaining function calls?**
A: LangGraph gives you:
- Visual workflow representation
- Easy routing logic
- State management built-in
- Ability to loop and branch

**Q: What's the difference between `add_edge` and `add_conditional_edges`?**
A: 
- `add_edge`: Always go to the same next node
- `add_conditional_edges`: Decide next node based on state

**Q: When do I use `END`?**
A: When you're done and want to stop the workflow. It's a special LangGraph constant.

**Q: Can agents modify the state?**
A: Yes! That's the whole point. Each agent reads state, does work, and updates state.

---

## 📖 Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)

---

## 🎉 You're Ready!

This is a complete, working LangGraph application. 

**Run it, understand it, modify it, and build upon it!**

Happy learning! 🚀