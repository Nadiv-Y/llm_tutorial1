from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI()

print("Sending request to OpenAI...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a comedian, tell me jokes."},
        {"role": "user", "content": "Why the sky is blue?"}
    ],
    temperature=0.7,
    max_tokens=500,
    stream=True
)   

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)

 