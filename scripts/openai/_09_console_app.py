"""
A simple console application for interacting with the agent.
"""

import asyncio
import json

from agents import Agent, Runner, SQLiteSession
from agents.mcp.server import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from dotenv import load_dotenv

from scripts.openai import MCP_SERVER_URL, OPENAI_MODEL

load_dotenv()

RUN_VERBOSE = False


titanic_mcp_server = MCPServerStreamableHttp(
    params=MCPServerStreamableHttpParams(
        url=MCP_SERVER_URL,
    )
)

agent = Agent(
    name="Elsa",
    instructions="You are a helpful agent.",
    mcp_servers=[titanic_mcp_server],
    model=OPENAI_MODEL,
)


async def main():
    await titanic_mcp_server.connect()

    print("=" * 50)
    print("Console Agent Chat")
    print("=" * 50)
    print("Type 'exit' or 'quit' to end the conversation\n")

    # Create a session to maintain conversation history
    session = SQLiteSession("console_chat")

    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()

            # Check for exit commands
            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye!")
                break

            # Skip empty input
            if not user_input:
                continue

            # Run the agent with the same session to maintain conversation history
            print("Agent: ", end="", flush=True)
            result = await Runner.run(agent, user_input, session=session)

            if RUN_VERBOSE:
                items = await session.get_items()
                for item in items:
                    print(json.dumps(item, indent=4))

            print(result.final_output)
            print()  # Add blank line for readability

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    finally:
        await titanic_mcp_server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
