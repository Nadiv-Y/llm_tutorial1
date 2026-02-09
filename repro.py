from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

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

tools = [get_weather, get_stock_price]

llm = ChatOpenAI(model="gpt-4o-mini")

llm_with_tools = llm.bind_tools(tools)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. use tools to answer the question if needed"),
    ("human", "{question}"),
    ("placeholder", "{agent_scratchpad}")
])

chain = prompt | llm_with_tools

def format_intermediate_steps(intermediate_steps):
    
    if not intermediate_steps:
        return []
    
    steps = []
    for action, observation in intermediate_steps:
        print(f"DEBUG: AIMessage ID: {action.id} (len: {len(action.id)})")
        if action.tool_calls:
            print(f"DEBUG: Tool Call ID: {action.tool_calls[0]['id']} (len: {len(action.tool_calls[0]['id'])})")
        steps.append(action)
        # steps.append(ToolMessage(content=observation, tool_call_id=action.id)) # Original buggy line
        # Use a safe placeholder or try to use the correct ID to see if it works, 
        # but for repro purposes we want to see it fail or at least see the values.
        # Let's keep the buggy line to confirm it fails, but printed values will be useful.
        steps.append(ToolMessage(content=observation, tool_call_id=action.id)) 
    return steps


def run_agent(user_question: str, max_iterations: int = 5):
    intermediate_steps = []
    for i in range(max_iterations):
        agent_scratchpad = format_intermediate_steps(intermediate_steps)
        response = chain.invoke({"question": user_question, "agent_scratchpad": agent_scratchpad})
        if response.tool_calls:
            result = response.tool_calls[0]
            function_name = result["name"]
            function_args = result["args"]
            print(function_name, function_args)
            observation = globals()[function_name].invoke(function_args)
            print(observation)
            intermediate_steps.append((response, observation))
        else:
            return response.content


print(run_agent("What is the weather like in Tel Aviv and what is the stock price of AAPL?"))