"""
A single, independent prompt.

Logs are found here: https://platform.openai.com/logs
"""

import dotenv
from openai import OpenAI

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-5-nano",
    input="In one sentence, what is the most likely reason why the project name `elsa` was chosen for this 2026 **Winter**nship quickstart project?",
)

print(response.output_text)
