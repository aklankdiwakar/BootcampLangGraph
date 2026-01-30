"""
Main Application - Simple Interactive Demo

This is the entry point. Run this to try the system!
"""

from workflow import create_workflow
from state import AgentState


def main():
    """Run the interactive demo"""

    print("=" * 70)
    print("  🤖 Simple Fusion HCM Agent - LangGraph Learning Demo")
    print("=" * 70)
    print("\nThis demo simulates HCM operations. Try these commands:")
    print("  • Assign HR Manager role to john.doe")
    print("  • Reset password for jane.smith")
    print("  • Unlock user bob.jones")
    print("\nType 'quit' to exit\n")
    print("=" * 70)

    # Build the workflow once
    app = create_workflow()

    while True:
        # Get user input
        user_input = input("\n💬 You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break

        if not user_input:
            continue

        # Create initial state with user's message
        initial_state = AgentState(
            messages=[user_input],
            action="",
            username="",
            extra_info="",
            result="",
            next_step="supervisor"
        )

        try:
            # Run the workflow!
            print("\n" + "─" * 70)
            final_state = app.invoke(initial_state)

            # Show the result
            print("\n" + "─" * 70)
            print("\n🤖 Agent:")
            print(f"   {final_state['result']}")
            print()

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different request.\n")


if __name__ == "__main__":
    main()