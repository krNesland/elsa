"""
Setting up an MCP server with tools.
"""

import json

import pandas as pd
from mcp.server.fastmcp import FastMCP

from scripts.openai import MCP_SERVER_PORT, TITANIC_DATA_PATH

mcp = FastMCP("titanic", port=MCP_SERVER_PORT)


def get_data() -> pd.DataFrame:
    return pd.read_csv(TITANIC_DATA_PATH)


@mcp.tool()
def get_titanic_passenger_names() -> str:
    """
    Get the index and name for each Titanic passenger.

    Args:
        None

    Returns a list of dictionaries with the index and name of each passenger.
    """
    data = get_data()
    return json.dumps(
        [
            {
                "idx": i,
                "name": name,
            }
            for i, name in enumerate(data["Name"].to_list())
        ]
    )


@mcp.tool()
def get_titanic_passenger_data(idx: int) -> str:
    """
    Get the data for a Titanic passenger, given the passenger's index.

    Args:
        idx: The index of the passenger.

    Returns a dictionary with the data for the passenger.
    """
    data = get_data()
    return json.dumps(data.iloc[idx].to_dict())


def main():
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
