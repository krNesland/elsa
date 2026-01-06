"""
Displaying the logprobs for a response.
"""

import dotenv
import numpy as np
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=dotenv.get_key(".env", "OPENAI_API_KEY"))

response = client.chat.completions.create(  # Because responses API does not support logprobs (?)
    model="gpt-4o-mini",  # Because logprobs are not supported with reasoning models
    messages=[
        {
            "role": "user",
            "content": "What is 38 * 62? Answer with only the number.",
        }
    ],
    logprobs=True,
    top_logprobs=5,
    max_completion_tokens=10,  # To not make it too long
)

for i, logprobs_content in enumerate(response.choices[0].logprobs.content):
    print(f"Token index {i}:")
    data = {
        "token": [],
        "logprob": [],
    }
    for token_candidate in logprobs_content.top_logprobs:
        data["token"].append(token_candidate.token)
        data["logprob"].append(token_candidate.logprob)

    df = pd.DataFrame(data)
    df["prob"] = np.exp(df["logprob"]) * 100
    print(df)
