"""
Querying the locally running MCP server.

Tools for web search and more are already shipped with the OpenAI SDK:
response = client.responses.create(
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input="What was a positive news story from today?"
)

Remote MCP servers can be used like this:
resp = client.responses.create(
    model="gpt-5",
    tools=[
        {
            "type": "mcp",
            "server_label": "dmcp",
            "server_description": "A Dungeons and Dragons MCP server to assist with dice rolling.",
            "server_url": "https://dmcp-server.deno.dev/sse",
            "require_approval": "never",
        },
    ],
    input="Roll 2d4+1",
)

It is also possible to define your own tools as simple Python functions and provide those to the model.

Note 1: Thought it would be possible to implement it in a more high-level way as seen here: https://platform.openai.com/docs/quickstart?tool-type=remote-mcp#extend-the-model-with-toolsHowever, seems like this is not working when the server is running locally. Therefore, having to implement the MCP client ourselves (https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients).
Note 2: This script sometimes takes a while to complete.
"""

import asyncio
import json

import dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from openai import OpenAI

from scripts.openai import MCP_SERVER_URL, OPENAI_MODEL

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))
conversation = client.conversations.create()


async def main():
    # Connect to a streamable HTTP server
    async with streamable_http_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")

            # Convert MCP tools to OpenAI format
            openai_tools = [
                {
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                    "strict": None,
                }
                for tool in tools.tools
            ]

            response = client.responses.create(
                model=OPENAI_MODEL,
                input="How many passengers are called William?",
                tools=openai_tools,
                conversation=conversation.id,
            )

            item = response.output[-1]
            assert item.type == "function_call"

            result = await session.call_tool(name=item.name, arguments=json.loads(item.arguments))
            response = client.responses.create(
                model=OPENAI_MODEL,
                input=[
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": str(result),
                    }
                ],
                conversation=conversation.id,
            )

            print(response.output_text)


if __name__ == "__main__":
    asyncio.run(main())
