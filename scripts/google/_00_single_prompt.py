"""
A single, independent prompt. Just to get a feel for the Google API and the responsiveness.
"""

import dotenv
from google import genai

client = genai.Client(api_key=dotenv.get_key(".env", "GOOGLE_API_KEY"))

response = client.models.generate_content(model="gemini-2.5-flash", contents="Explain how AI works in a few words")
print(response.text)
