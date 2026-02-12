from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
try:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
except ImportError:
    from langchain_classic.agents import AgentExecutor
    from langchain_classic.agents import create_tool_calling_agent
import os
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

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
def search_web(query: str):
    """Search the web for information"""
    response = tavily_client.search(query=query, max_results=3)
    results = [{"title": result["title"], "url": result["url"], "content": result["content"]} for result in response["results"]]
    return results[1]

tools = [get_weather, search_web]

llm = ChatOpenAI(model="gpt-4o-mini")

llm_with_tools = llm.bind_tools(tools)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. use tools to answer the question if needed"),
    ("human", "{question}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm_with_tools, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(agent_executor.invoke({"question": "What is the weather like in Tel Aviv? and what is the population of Tel Aviv in 2026?"}))



