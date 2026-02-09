
import time
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


@tool
def get_stock_price(stock_symbol):
    """Get the stock price of a company"""
    stock_data = {
        "AAPL": "150",
        "GOOGL": "2500",
        "MSFT": "300"
    }
    return stock_data.get(stock_symbol, "Unknown stock")

@tool
def calculate(expression: str):
    """Calculate the sum of two numbers"""
    return eval(expression)

tools = [get_weather, get_stock_price, calculate]

llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

llm_with_tools = llm.bind_tools(tools)

messages = [HumanMessage(content="What is the result of 2 + 2, and what is the weather like in Haifa and in Jerusalem?")]


final_chunk = None


for chunk in llm_with_tools.stream(messages):

    if chunk.content:
        print(chunk.content, end="", flush=True)

    if final_chunk is None:
        final_chunk = chunk
    else:
        final_chunk += chunk

    if chunk.tool_call_chunks:
        print(".", end="", flush=True)
        time.sleep(0.1)


if final_chunk and final_chunk.tool_calls:
    print("\n")
    print(f"num of tools: {len(final_chunk.tool_calls)}")
    messages.append(final_chunk)

    for tool_call in final_chunk.tool_calls:
        function_name = tool_call["name"]
        function_args = tool_call["args"]
        print(function_name, function_args)

        result = globals()[function_name].invoke(function_args)
        print(result)
            
        messages.append(ToolMessage(tool_call_id=tool_call["id"], content=str(result)))

for chunk in llm_with_tools.stream(messages):
    if chunk.content:
        print(chunk.content, end="", flush=True)
