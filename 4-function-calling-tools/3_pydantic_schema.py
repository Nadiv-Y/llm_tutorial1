from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()

client = OpenAI()


def save_contact(name: str, phone: str, email: str, address: str):
    return json.dumps({"name": name, "phone": phone, "email": email, "address": address})


class Contact(BaseModel):
    name: str = Field(description="The name of the contact")
    phone: str = Field(description="The phone number of the contact")
    email: str = Field(description="The email address of the contact")
    address: str = Field(description="The address of the contact")



tools = [
    {
        "type": "function",
        "function": {
            "name": "save_contact",
            "description": "Save a contact's information",
            "parameters": Contact.model_json_schema()
        }
    }
]


text = """
Hi I'm Max Epstein, I live in Jerusalem and I'm a lawyer. My phone number is 050-1234567 and my email is max.epstein@example.com. My address is 123 Main St, Jerusalem, Israel.
"""


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extract the contact information from the text"},
        {"role": "user", "content": text}
    ],
    tools=tools
)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    print(function_name, function_args)

    result = globals()[function_name](**function_args)

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Compare name and contact email prefix and return true if they match"},
        {"role": "user", "content": text},
        {"role": "assistant", "tool_calls": [tool_call.model_dump()]},
        {"role": "tool", "tool_call_id": tool_call.id, "content": result}
    ]
)

print(final_response.choices[0].message.content)