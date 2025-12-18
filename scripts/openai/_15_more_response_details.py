"""
Displaying a bit more of what is stored in the response object.

Trying to force some reasoning by giving the model an impossible math problem. However, seems like OpenAI is hiding the reasoning as you can see that reasoning tokeans are used.
"""

import dotenv
from openai import OpenAI

from scripts.openai import OPENAI_MODEL

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))

response = client.responses.create(
    model=OPENAI_MODEL,
    input="I am currently 6 years older than my brother. In 10 years, I will be exactly three times as old as he was 5 years ago. If the sum of our ages in 2 years will be 14, how old is my brother right now?",
    reasoning={"effort": "medium"},
)

# Pretty print the full response for debugging
print(response.model_dump_json(indent=2))
