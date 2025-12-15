"""
Query with image.
"""

import dotenv
from openai import OpenAI

from scripts.openai import OPENAI_MODEL

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))


# Function to create a file with the Files API
def create_file(file_path):
    with open(file_path, "rb") as file_content:
        result = client.files.create(
            file=file_content,
            purpose="vision",
        )
        return result.id


# Getting the file ID
file_id = create_file("data/unknown.jpg")

response = client.responses.create(
    model=OPENAI_MODEL,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Who is this television character?"},
                {
                    "type": "input_image",
                    "file_id": file_id,
                },
            ],
        }
    ],
)

print(response.output_text)
