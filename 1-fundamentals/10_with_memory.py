#clarity
#specificity
#context
#constraints


from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break   
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        top_p=0.9,
        max_tokens=100,
    )

    assistant_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_response})

    print("Assistant:", assistant_response)


