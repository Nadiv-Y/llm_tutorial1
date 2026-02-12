from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from tavily import TavilyClient
from typing_extensions import TypedDict
import os

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatOpenAI(model="gpt-4o-mini")

class State(TypedDict):
    query: str
    result: str
    summary: str


def search_web(state: State) -> State:
    """Search the web for information"""
    response = tavily_client.search(query=state["query"], max_results=3)
    results = [{"title": result["title"], "url": result["url"], "content": result["content"]} for result in response["results"]]
    state["result"] = str(results[0])
    return state

def summarize(state: State) -> State:
    """Summarize the result"""
    messages = [SystemMessage(content="You are a good summarizer, summarize the text"), HumanMessage(content=state["result"])]
    state["summary"] = llm.invoke(messages).content
    return state

workflow = StateGraph(State)

workflow.add_node("search_web", search_web)
workflow.add_node("summarize", summarize)

workflow.add_edge(START, "search_web")
workflow.add_edge("search_web", "summarize")
workflow.add_edge("summarize", END)


app = workflow.compile()

result = app.invoke({"query": "What is the weather like in Tel Aviv?", "result":"", "summary":""})
print(result["summary"])