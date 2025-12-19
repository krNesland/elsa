"""
Retrieving a conversation by ID.

Could be useful if one want to use the OpenAI servers as the ground truth message history (instead of keeping track of the messages in some local data structure).
"""

import dotenv
from openai import OpenAI

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))

# Example conversation ID
conversation_id = "conv_6943c876a7808195941df3b7fa0fc4dd01782d79c2674228"

conversation = client.conversations.retrieve(conversation_id)
print(conversation)
print("-" * 100)

items = client.conversations.items.list(conversation_id, limit=10, order="asc")
for i, item in enumerate(items):
    print(f"Item {i}:")
    print(item)
    print("-" * 100)
