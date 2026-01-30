"""
LangGraph Workflow - Connecting Everything Together

This is THE CORE of LangGraph!
We define:
1. Nodes (the agents)
2. Edges (how to move between agents)
3. Routing logic (which agent to go to next)
"""

import sys
import os

# Ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from langgraph.graph import StateGraph, END
from state import AgentState
from supervisor import supervisor_agent
from agents import role_agent, password_agent, unlock_agent


def create_workflow():
    """
    This function builds the entire agent workflow.

    Think of it like building a flowchart!
    """

    print("🔧 Building the workflow...")

    # Step 1: Create the graph with our state
    workflow = StateGraph(AgentState)

    # Step 2: Add nodes (each node is an agent)
    print("   Adding nodes (agents)...")
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("role_agent", role_agent)
    workflow.add_node("password_agent", password_agent)
    workflow.add_node("unlock_agent", unlock_agent)

    # Step 3: Define the routing function
    # This function looks at the state and decides where to go next
    def route_to_next(state: AgentState) -> str:
        """
        This is the 'traffic controller'.
        It reads state["next_step"] and decides where to route.
        """
        next_step = state["next_step"]

        if next_step == "end":
            return END  # Special LangGraph constant meaning "we're done!"
        else:
            return next_step  # Go to that agent

    # Step 4: Set the starting point
    workflow.set_entry_point("supervisor")

    # Step 5: Add edges (connections between nodes)
    # From supervisor, route based on the decision
    workflow.add_conditional_edges(
        "supervisor",  # From this node
        route_to_next,  # Use this function to decide
        {
            "role_agent": "role_agent",
            "password_agent": "password_agent",
            "unlock_agent": "unlock_agent",
            END: END
        }
    )

    # From each sub-agent, always go to END
    workflow.add_edge("role_agent", END)
    workflow.add_edge("password_agent", END)
    workflow.add_edge("unlock_agent", END)

    # Step 6: Compile the graph
    print("   Compiling the graph...")
    app = workflow.compile()

    print("   ✓ Workflow ready!\n")

    return app


# Create the compiled workflow and export it
# This is what langgraph.json references
agent_workflow = create_workflow()

# Visual representation of our workflow:
"""
           START
             ↓
        [Supervisor] ← Analyzes request
             ↓
        (Decision)
       /     |     \
      /      |      \
[Role]  [Password] [Unlock] ← Sub-agents do the work
      \      |      /
       \     |     /
            END
"""

if __name__ == "__main__":
    # Test the workflow
    print("=" * 60)
    print("Testing the Complete Workflow")
    print("=" * 60)

    app = create_workflow()

    # Create initial state
    initial_state = AgentState(
        messages=["Assign HR Manager role to john.doe"],
        action="",
        username="",
        extra_info="",
        result="",
        next_step="supervisor"
    )

    print("\n📥 Initial state:")
    print(f"   User message: {initial_state['messages'][0]}")

    # Run the workflow!
    print("\n🚀 Running the workflow...")
    print("=" * 60)

    final_state = app.invoke(initial_state)

    print("\n" + "=" * 60)
    print("📤 Final Result:")
    print("=" * 60)
    print(f"Action performed: {final_state['action']}")
    print(f"Username: {final_state['username']}")
    print(f"Result: {final_state['result']}")