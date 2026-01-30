"""
Sub-Agents - The Workers

These agents do the actual work:
1. Role Agent - Assigns roles
2. Password Agent - Resets passwords
3. Unlock Agent - Unlocks users

For learning, we'll SIMULATE the API calls instead of making real ones.
"""

from state import AgentState
import random
import string


def role_agent(state: AgentState) -> AgentState:
    """
    Assigns a role to a user.

    In real life, this would call the Fusion HCM API.
    For learning, we'll just simulate it!
    """

    print(f"\n👤 ROLE AGENT: Assigning role '{state['extra_info']}' to user '{state['username']}'")

    # Simulate API call
    print("   📡 Calling Fusion HCM API... (simulated)")
    print(f"   POST /api/users/{state['username']}/roles")
    print(f"   Body: {{ 'role': '{state['extra_info']}' }}")

    # Simulate success
    state["result"] = f"✓ Successfully assigned role '{state['extra_info']}' to {state['username']}"
    state["next_step"] = "end"

    print(f"   {state['result']}")

    return state


def password_agent(state: AgentState) -> AgentState:
    """
    Resets a user's password.

    Generates a random password and 'resets' it.
    """

    print(f"\n🔑 PASSWORD AGENT: Resetting password for user '{state['username']}'")

    # Generate a random password
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    print("   📡 Calling Fusion HCM API... (simulated)")
    print(f"   PATCH /api/users/{state['username']}")
    print(f"   Body: {{ 'password': '***hidden***' }}")

    # Simulate success
    state["result"] = f"✓ Password reset for {state['username']}\n   New password: {new_password}"
    state["next_step"] = "end"

    print(f"   {state['result']}")

    return state


def unlock_agent(state: AgentState) -> AgentState:
    """
    Unlocks a locked user account.
    """

    print(f"\n🔓 UNLOCK AGENT: Unlocking user '{state['username']}'")

    print("   📡 Calling Fusion HCM API... (simulated)")
    print(f"   PATCH /api/users/{state['username']}")
    print(f"   Body: {{ 'locked': false }}")

    # Simulate success
    state["result"] = f"✓ Successfully unlocked user {state['username']}"
    state["next_step"] = "end"

    print(f"   {state['result']}")

    return state


# Test each agent
if __name__ == "__main__":
    print("Testing Role Agent:")
    test_state = AgentState(
        messages=["test"],
        action="assign_role",
        username="john.doe",
        extra_info="HR Manager",
        result="",
        next_step="role_agent"
    )
    role_agent(test_state)

    print("\n" + "=" * 50)
    print("Testing Password Agent:")
    test_state = AgentState(
        messages=["test"],
        action="reset_password",
        username="jane.smith",
        extra_info="",
        result="",
        next_step="password_agent"
    )
    password_agent(test_state)

    print("\n" + "=" * 50)
    print("Testing Unlock Agent:")
    test_state = AgentState(
        messages=["test"],
        action="unlock_user",
        username="bob.jones",
        extra_info="",
        result="",
        next_step="unlock_agent"
    )
    unlock_agent(test_state)