"""
Simple State Definition for LangGraph

This is the most important concept in LangGraph!
The state holds all information as it flows through the agents.
"""

from typing import TypedDict, List


class AgentState(TypedDict):
    """
    This is like a shared notebook that all agents can read and write to.
    As the state moves from agent to agent, they add information to it.
    """

    # The conversation messages
    messages: List[str]  # Simple list of messages

    # What the user wants to do
    action: str  # "assign_role", "reset_password", or "unlock_user"

    # Who to perform the action on
    username: str  # e.g., "john.doe"

    # Extra information (like role name for assignment)
    extra_info: str  # e.g., "HR Manager"

    # Did it work?
    result: str  # The final result message

    # Which agent should handle this next?
    next_step: str  # "supervisor", "role_agent", "password_agent", "unlock_agent", or "end"


# Example of how state flows:
"""
Initial State:
{
    "messages": ["Assign HR Manager role to john.doe"],
    "action": "",
    "username": "",
    "extra_info": "",
    "result": "",
    "next_step": "supervisor"
}

After Supervisor:
{
    "messages": ["Assign HR Manager role to john.doe"],
    "action": "assign_role",
    "username": "john.doe",
    "extra_info": "HR Manager",
    "result": "",
    "next_step": "role_agent"
}

After Role Agent:
{
    "messages": ["Assign HR Manager role to john.doe"],
    "action": "assign_role",
    "username": "john.doe",
    "extra_info": "HR Manager",
    "result": "✓ Successfully assigned HR Manager to john.doe",
    "next_step": "end"
}
"""