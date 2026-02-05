from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()


def get_weather(city):
    """Get the weather in a city"""
    weather_data = {
        "Tel Aviv": "28 degrees Celsius",
        "Jerusalem": "25 degrees Celsius",
        "Haifa": "26 degrees Celsius"
    }
    return weather_data.get(city, "Unknown city")


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather in a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get the weather for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "What is the weather like in Tel Aviv right now?"}
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
        {"role": "user", "content": "What is the weather like in Tel Aviv right now?"},
        {"role": "assistant", "tool_calls": [tool_call.model_dump()]},
        {"role": "tool", "tool_call_id": tool_call.id, "content": result}
    ]
)

print(final_response.choices[0].message.content)