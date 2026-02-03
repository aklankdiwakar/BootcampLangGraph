"""
Main Application - Simple Interactive Demo

This is the entry point. Run this to try the system!
"""

import sys
import os

# Ensure imports work from any directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from workflow import create_workflow
from state import AgentState


def main():
    """Run the interactive demo"""

    print("=" * 70)
    print("  🤖 Simple Fusion HCM Agent - LangGraph Learning Demo")
    print("=" * 70)
    print("\nThis demo simulates HCM operations. Try these commands:")
    print("  • I am Aklank and my user id is aklankdiwakar")
    print("  • Assign me Admin role for HCM")
    print("  • Reset password for jane.smith")
    print("  • Unlock user bob.jones")
    print("\n💡 The system will remember your information!")
    print("\nType 'quit' to exit\n")
    print("=" * 70)

    # Build the workflow once
    app = create_workflow()

    # 🆕 Initialize persistent memory across the session
    session_memory = {}

    while True:
        # Get user input
        user_input = input("\n💬 You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break

        if not user_input:
            continue

        # Create initial state with user's message
        # 🆕 Preserve memory from previous interactions
        initial_state = AgentState(
            messages=[user_input],
            action="",
            username="",
            extra_info="",
            result="",
            next_step="supervisor",
            user_memory=session_memory  # 🆕 Pass the memory!
        )

        try:
            # Run the workflow!
            print("\n" + "─" * 70)
            final_state = app.invoke(initial_state)

            # 🆕 Update session memory with any new information
            if final_state.get("user_memory"):
                session_memory = final_state["user_memory"]

            # Show the result
            print("\n" + "─" * 70)
            print("\n🤖 Agent:")
            print(f"   {final_state['result']}")

            # 🆕 Show current memory if it exists
            if session_memory:
                print("\n   📝 Remembered:")
                for key, value in session_memory.items():
                    print(f"      • {key}: {value}")
            print()

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different request.\n")


if __name__ == "__main__":
    main()