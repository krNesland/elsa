"""
Setting up an MCP server with tools.
"""

import json

import pandas as pd
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("titanic", port=8000)

data = pd.read_csv("data/titanic.csv")


@mcp.tool()
def get_titanic_passenger_names() -> str:
    """
    Get the index and name for each Titanic passenger.
    """
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
    """
    return json.dumps(data.iloc[idx].to_dict())


def main():
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
