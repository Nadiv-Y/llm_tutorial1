
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

llm = ChatOpenAI(model="gpt-4o-mini")

llm_with_tools = llm.bind_tools(tools)

queries = [
    "What is the weather like in Tel Aviv?",
    "What is the weather like in Jerusalem and price of AAPL stock?",
    "What is the result of 2 + 2, and what is the weather like in Haifa and in Jerusalem?"
]

for query in queries:
    response = llm_with_tools.invoke(query)

    print(response)

    if response.tool_calls:
        messages = [HumanMessage(content=query), response]
        
        for tool_call in response.tool_calls:
            function_name = tool_call["name"]
            function_args = tool_call["args"]
            print(function_name, function_args)

            result = globals()[function_name].invoke(function_args)
            print(result)
            
            messages.append(ToolMessage(tool_call_id=tool_call["id"], content=str(result)))

        final_response = llm_with_tools.invoke(messages)

        print(final_response.content)
