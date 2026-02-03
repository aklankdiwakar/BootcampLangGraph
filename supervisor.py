"""
Supervisor Agent - The Brain of the System

This agent looks at what the user wants and decides:
- Which action to perform (assign role, reset password, unlock user)
- Which agent should handle it
"""

from langchain_openai import ChatOpenAI
from state import AgentState
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
load_dotenv()


def supervisor_agent(state: AgentState) -> AgentState:
    """
    The supervisor reads the user's message and figures out what to do.

    Think of it like a receptionist who directs you to the right department!
    """

    print("\n🧠 SUPERVISOR: Analyzing the request...")
    user_message = state["messages"][0]
    print(f"   User said: '{user_message}'")

    # Use GPT to understand what the user wants

    llm = ChatOllama(model="qwen2:1.5b")
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
    You are analyzing a user request for an HCM system.

    User request: "{user_message}"

    Determine:
    1. What action? (assign_role, reset_password, or unlock_user)
    2. Which username?
    3. Any extra info? (like role name if assigning a role)

    Respond in this EXACT format:
    ACTION: <action>
    USERNAME: <username>
    EXTRA: <extra info or "none">

    Example:
    ACTION: assign_role
    USERNAME: john.doe
    EXTRA: HR Manager
    """

    response = llm.invoke(prompt)
    decision = response.content

    print(f"   GPT's analysis:\n{decision}")

    # Parse GPT's response
    lines = decision.strip().split('\n')
    for line in lines:
        if line.startswith("ACTION:"):
            state["action"] = line.replace("ACTION:", "").strip()
        elif line.startswith("USERNAME:"):
            state["username"] = line.replace("USERNAME:", "").strip()
        elif line.startswith("EXTRA:"):
            extra = line.replace("EXTRA:", "").strip()
            state["extra_info"] = extra if extra != "none" else ""

    # Decide which agent to route to
    action_to_agent = {
        "assign_role": "role_agent",
        "reset_password": "password_agent",
        "unlock_user": "unlock_agent"
    }

    state["next_step"] = action_to_agent.get(state["action"], "end")

    print(f"   ✓ Decision: Route to '{state['next_step']}'")

    return state


# Test it standalone
if __name__ == "__main__":
    # Example test
    test_state = AgentState(
        messages=["Assign HR Manager role to john.doe"],
        action="",
        username="",
        extra_info="",
        result="",
        next_step="supervisor"
    )

    result = supervisor_agent(test_state)
    print(f"\nFinal state: {result}")