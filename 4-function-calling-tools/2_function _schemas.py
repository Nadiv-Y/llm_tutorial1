from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()


def book_flight(origin: str, destination: str, passengers: int = 1):
    """Book a flight to a city"""
    return f"Flight booked to {destination} from {origin} for {passengers} passengers"


tools = [
    {
        "type": "function",
        "function": {
            "name": "book_flight",
            "description": "Book a flight between two cities for a given number of passengers",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Departure city"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination city"
                    },
                    "passengers": {
                        "type": "integer",
                        "description": "Number of passengers"
                    }
                },
                "required": ["origin", "destination"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Book a flight to Tel Aviv from Jerusalem for 2 passengers"}
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
        {"role": "user", "content": "Book a flight to Tel Aviv from Jerusalem for 2 passengers"},
        {"role": "assistant", "tool_calls": [tool_call.model_dump()]},
        {"role": "tool", "tool_call_id": tool_call.id, "content": result}
    ]
)

print(final_response.choices[0].message.content)