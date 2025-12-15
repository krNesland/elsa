"""
A single, independent prompt.

Responses are found here: https://platform.openai.com/logs?api=responses
"""

import dotenv
from openai import OpenAI

from scripts.openai import OPENAI_MODEL

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))

response = client.responses.create(
    model=OPENAI_MODEL,
    input="In one sentence, what is the most likely reason why the project name `elsa` was chosen for this 2026 **Winter**nship quickstart project?",
)

print(response.output_text)
