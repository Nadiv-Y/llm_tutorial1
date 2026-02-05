from dotenv import load_dotenv
from openai import OpenAI
import json
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI()


def get_weather(city, unit="celsius"):
    """Get the weather in a city"""
    weather_data = {
        "Tel Aviv": f"28 degrees {unit}",
        "Jerusalem": f"25 degrees {unit}",
        "Haifa": f"26 degrees {unit}"
    }
    return weather_data.get(city, "Unknown city")


def get_time(city):
    """Get the time in a city"""
    time_data = {
        "Tel Aviv": "12:00 PM",
        "Jerusalem": "12:00 PM",
        "Haifa": "12:00 PM"
    }
    return time_data.get(city, "Unknown city")

class Weather(BaseModel):
    city: str = Field(description="The city to get the weather for")
    unit: str = Field(description="The unit of temperature", default="celsius")

class Time(BaseModel):
    city: str = Field(description="The city to get the time for")


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the weather in a city",
            "parameters": Weather.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the time in a city",
            "parameters": Time.model_json_schema()
        }
    }
]

queries = [
    "What is the weather like in Tel Aviv right now?",
    "What is the time in Jerusalem right now?",
    "What is the weather like in Haifa in fahrenheit?",
    "Why did Bnei Yehuda defeat Beitar Jerusalem?"
]

for query in queries:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": query}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_weather"}}
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
                {"role": "user", "content": query},
                {"role": "assistant", "tool_calls": [tool_call.model_dump()]},
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            ]
        )

        print(final_response.choices[0].message.content)

    else:
        print(response.choices[0].message.content)


