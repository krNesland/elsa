"""
Going beyond a single independent prompt.

Conversations are found here: https://platform.openai.com/logs?api=conversations
"""

import dotenv
from openai import OpenAI

from scripts.openai import OPENAI_MODEL

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))
conversation = client.conversations.create()

response = client.responses.create(
    model=OPENAI_MODEL,
    input="In one sentence, what is the most likely reason why the project name `elsa` was chosen for this 2026 **Winter**nship quickstart project?",
    conversation=conversation.id,
)

response = client.responses.create(
    model=OPENAI_MODEL,
    input="What was my first prompt?",
    conversation=conversation.id,
)

print("\nResponse: ", response.output_text)
