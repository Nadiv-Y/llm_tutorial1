
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

load_dotenv()

@tool
def get_weather(city):
    """Get the weather in a city"""
    weather_data = {
        "Tel Aviv": "28 degrees Celsius",
        "Jerusalem": "25 degrees Celsius",
        "Haifa": "26 degrees Celsius"
    }
    return weather_data.get(city, "Unknown city")

tools = [get_weather]

llm = ChatOpenAI(model="gpt-4o-mini")

llm_with_tools = llm.bind_tools(tools)

response = llm_with_tools.invoke("What is the weather like in Tel Aviv?")

if response.tool_calls:
    tool_call = response.tool_calls[0]
    function_name = tool_call["name"]
    function_args = tool_call["args"]

    print(response)
    print(function_name, function_args)

    result = globals()[function_name].invoke(function_args)

    print(result)

    messages = [
        HumanMessage(content="What is the weather like in Tel Aviv?"),
        response,
        ToolMessage(tool_call_id=tool_call["id"], content=result)
    ]

    final_response = llm_with_tools.invoke(messages)

    print(final_response.content)
