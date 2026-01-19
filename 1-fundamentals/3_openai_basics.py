from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

print("Sending request to OpenAI...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a comedian, tell me jokes."},
        {"role": "user", "content": "Why the sky is blue?"}
    ],
    temperature=0.7,
    max_tokens=500
)   

usage = response.usage

print("Tokens used:", usage.total_tokens)
print("Prompt tokens used:", usage.prompt_tokens)
print("Completion tokens used:", usage.completion_tokens)
print("Response from OpenAI:", response.choices[0].message.content) 