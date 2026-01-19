import requests
import json


response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": "Why is the sky blue?",
    },
    stream=True
)


for line in response.iter_lines():
    data = json.loads(line)
    print(data.get('response', ''), end='', flush=True)

