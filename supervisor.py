"""
Supervisor Agent - The Brain of the System

This agent looks at what the user wants and decides:
- Which action to perform (assign role, reset password, unlock user)
- Which agent should handle it
"""

import sys
import os

# Ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from langchain_openai import ChatOpenAI
from state import AgentState
from dotenv import load_dotenv
from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI
load_dotenv()


def supervisor_agent(state: AgentState) -> AgentState:
    """
    The supervisor reads the user's message and figures out what to do.

    Think of it like a receptionist who directs you to the right department!
    """

    print("\n🧠 SUPERVISOR: Analyzing the request...")

    user_message = state["messages"][-1]  # Get the latest message
    print(f"   User said: '{user_message}'")

    # Check if we have memory from previous conversations
    memory_context = ""
    if state.get("user_memory"):
        memory = state["user_memory"]
        memory_context = f"\n\nRemembered information about the user:\n"
        if memory.get("name"):
            memory_context += f"- Name: {memory['name']}\n"
        if memory.get("user_id"):
            memory_context += f"- User ID: {memory['user_id']}\n"
        if memory.get("email"):
            memory_context += f"- Email: {memory['email']}\n"
        print(f"   📝 Using stored memory: {memory}")

    # Use GPT to understand what the user wants
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm = ChatOCIGenAI(
        model_id="cohere.command-r-plus-08-2024",
        service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
        compartment_id=
        "ocid1.compartment.oc1..aaaaaaaakggm6zsow2fefyjbtvftjdd7bxkgmvazunepkpi34o6hpzzequca",
        model_kwargs={"temperature": 0.7, "max_tokens": 500},
        auth_profile='omcsmig_chicago'
    )
    prompt = f"""
    You are analyzing a user request for an HCM system.
    {memory_context}
    
    Current user request: "{user_message}"
    
    First, check if the user is introducing themselves or providing their information:
    - If they say "I am [name]" or "My name is [name]" → Extract their name
    - If they say "my user id is [id]" or "my username is [id]" → Extract their user_id
    - If they say "my email is [email]" → Extract their email
    
    If this is just information storage (not an action request), respond with:
    ACTION: store_info
    USERNAME: none
    EXTRA: none
    NAME: [their name if mentioned, else "none"]
    USER_ID: [their user_id if mentioned, else "none"]
    EMAIL: [their email if mentioned, else "none"]
    
    If the user wants to perform an action:
    1. What action? (assign_role, reset_password, or unlock_user)
    2. Which username? (Use their stored user_id if they say "me" or "my account")
    3. Any extra info? (like role name if assigning a role)
    
    Respond in this EXACT format:
    ACTION: <action>
    USERNAME: <username or their stored user_id>
    EXTRA: <extra info or "none">
    NAME: none
    USER_ID: none
    EMAIL: none
    
    Examples:
    
    User: "I am Aklank and my user id is aklankdiwakar"
    Response:
    ACTION: store_info
    USERNAME: none
    EXTRA: none
    NAME: Aklank
    USER_ID: aklankdiwakar
    EMAIL: none
    
    User: "Assign me Admin role for HCM" (and user_id is stored as aklankdiwakar)
    Response:
    ACTION: assign_role
    USERNAME: aklankdiwakar
    EXTRA: Admin role for HCM
    NAME: none
    USER_ID: none
    EMAIL: none
    
    User: "Reset password for john.doe"
    Response:
    ACTION: reset_password
    USERNAME: john.doe
    EXTRA: none
    NAME: none
    USER_ID: none
    EMAIL: none
    """

    response = llm.invoke(prompt)
    decision = response.content

    print(f"   GPT's analysis:\n{decision}")

    # Parse GPT's response
    lines = decision.strip().split('\n')
    parsed = {}
    for line in lines:
        if line.startswith("ACTION:"):
            parsed["action"] = line.replace("ACTION:", "").strip()
        elif line.startswith("USERNAME:"):
            parsed["username"] = line.replace("USERNAME:", "").strip()
        elif line.startswith("EXTRA:"):
            extra = line.replace("EXTRA:", "").strip()
            parsed["extra"] = extra if extra != "none" else ""
        elif line.startswith("NAME:"):
            name = line.replace("NAME:", "").strip()
            parsed["name"] = name if name != "none" else ""
        elif line.startswith("USER_ID:"):
            user_id = line.replace("USER_ID:", "").strip()
            parsed["user_id"] = user_id if user_id != "none" else ""
        elif line.startswith("EMAIL:"):
            email = line.replace("EMAIL:", "").strip()
            parsed["email"] = email if email != "none" else ""

    # Handle information storage
    if parsed.get("action") == "store_info":
        # Initialize user_memory if it doesn't exist
        if not state.get("user_memory"):
            state["user_memory"] = {}

        # Store the information
        if parsed.get("name"):
            state["user_memory"]["name"] = parsed["name"]
            print(f"   💾 Stored name: {parsed['name']}")
        if parsed.get("user_id"):
            state["user_memory"]["user_id"] = parsed["user_id"]
            print(f"   💾 Stored user_id: {parsed['user_id']}")
        if parsed.get("email"):
            state["user_memory"]["email"] = parsed["email"]
            print(f"   💾 Stored email: {parsed['email']}")

        # Set friendly response
        state["result"] = f"✓ Got it! I've remembered your information."
        state["next_step"] = "end"
        state["action"] = "store_info"
        print(f"   ✓ Information stored successfully")
        return state

    # Handle regular actions
    state["action"] = parsed.get("action", "")
    state["username"] = parsed.get("username", "")
    state["extra_info"] = parsed.get("extra", "")

    # Decide which agent to route to
    action_to_agent = {
        "assign_role": "role_agent",
        "reset_password": "password_agent",
        "unlock_user": "unlock_agent"
    }

    next_agent = action_to_agent.get(parsed.get("action"), "end")
    state["next_step"] = next_agent
    state["current_agent"] = "supervisor"
    state["status"] = "in_progress"

    print(f"   ✓ Decision: Route to '{next_agent}'")

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