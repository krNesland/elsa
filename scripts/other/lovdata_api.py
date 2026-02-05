"""
Lovdata API Client

Functions for interacting with Lovdata's public API endpoints.
API Documentation: https://api.lovdata.no/swagger
"""

from typing import Any

import requests
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

LOVDATA_API_BASE_URL = "https://api.lovdata.no"


@function_tool
def list_public_data() -> dict[str, Any]:
    """
    List all available public data files from Lovdata API.

    Returns:
        dict: JSON response containing list of available files

    Raises:
        requests.HTTPError: If the API request fails
    """
    url = f"{LOVDATA_API_BASE_URL}/v1/publicData/list"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


agent = Agent(
    name="Elsa",
    instructions="Respond in Norwegian.",
    model="gpt-5.2",
    tools=[list_public_data],
)

result = Runner.run_sync(agent, input="List all available public data files from Lovdata API.")
print(result.final_output)
