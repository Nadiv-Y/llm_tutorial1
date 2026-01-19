import ollama


MODEL_NAME = "llama3.2"

print(f'Sending request to {MODEL_NAME}')

try:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": "Why is the sky blue?"}
        ]
    )

    content = response.message.content
    print("\nResponse from Ollama:", content)
except Exception as e:
    print(f"Error: {e}")