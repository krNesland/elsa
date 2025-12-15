"""
A simple agent on the OpenAI Agents SDK.

Run details are found here: https://platform.openai.com/logs?api=traces

https://github.com/openai/openai-agents-python
"""

import asyncio

from agents import Agent, Runner
from agents.mcp.server import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from dotenv import load_dotenv

from scripts.openai import OPENAI_MODEL

load_dotenv()


titanic_mcp_server = MCPServerStreamableHttp(
    params=MCPServerStreamableHttpParams(
        url="http://localhost:8000/mcp",
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
    try:
        result = await Runner.run(agent, input="What fare did Telma Matilda Storm pay for her ticket?")
        print(result.final_output)
    finally:
        await titanic_mcp_server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
