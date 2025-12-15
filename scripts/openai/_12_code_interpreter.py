"""
Give the model access to a remote container.

Check out the logs here to see the code that was executed: https://platform.openai.com/logs?api=responses

Note how the code interpreter would be able to answer similar questions as the MCP tools, but without the need to implement the tools ourselves.
"""

from dotenv import load_dotenv
from openai import OpenAI

from scripts.openai import OPENAI_MODEL

load_dotenv()

try:
    client = OpenAI()

    with open("data/titanic.csv", "rb") as file:
        titanic_file = client.files.create(file=file, purpose="user_data")

    container = client.containers.create(name="test-container", memory_limit="1g", file_ids=[titanic_file.id])

    response = client.responses.create(
        model=OPENAI_MODEL,
        tools=[
            {
                "type": "code_interpreter",
                "container": container.id,
            }
        ],
        tool_choice="required",
        input=[
            {
                "role": "user",
                "content": "What fare did Mr. Kevin Malone pay for his ticket? Use the python tool to analyze the data and provide the answer.",
            }
        ],
    )

    print(response.output_text)
finally:
    client.containers.delete(container.id)
