"""
Letting the model call tools.

Probably not working because: The fundamental problem is that OpenAI's servers cannot access your local localhost:8000. When you send a request to OpenAI's API with an MCP server URL, OpenAI tries to connect to that URL from their servers, not from your machine.

Therefore, can't use the local MCP server with the high-level API. Need to make it more low-level.
"""

import dotenv
from openai import OpenAI

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))


tools = [
    {
        "type": "mcp",
        "server_label": "titanic",
        "server_description": "A server that exposes data about the Titanic passengers.",
        "server_url": "http://localhost:8000/mcp",
        "require_approval": "never",
    },
]

response = client.responses.create(
    model="gpt-5-nano",
    input="What fare did Mr. William Thompson Sloper pay?",
    tools=tools,
)

print(response.output_text)
