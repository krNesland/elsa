"""
Providing some instructions (system prompt) to the model.
"""

import dotenv
from openai import OpenAI

from scripts.openai import OPENAI_MODEL

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))

response = client.responses.create(
    model=OPENAI_MODEL,
    input="In one sentence, what is the most likely reason why the project name `elsa` was chosen for this 2026 **Winter**nship quickstart project?",
    instructions="Answer in a way that a six year old would understand.",
)

print(response.output_text)
