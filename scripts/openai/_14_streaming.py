"""
Streaming responses from the model.
"""

import dotenv
from openai import OpenAI

from scripts.openai import OPENAI_MODEL

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))

stream = client.responses.create(
    model=OPENAI_MODEL,
    instructions="Be overly positive and enthusiastic.",
    input=[
        {
            "role": "user",
            "content": "Who is Kevin Malone?",
        },
    ],
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(f"{event.sequence_number}: {event.delta}")
