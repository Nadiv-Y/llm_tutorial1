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
    need_more_info: bool
    final_answer: str


def search_web(state: State) -> State:
    """Search the web for information"""
    print("searching the web...")
    response = tavily_client.search(query=state["query"], max_results=3)
    results = [{"title": result["title"], "url": result["url"], "content": result["content"]} for result in response["results"]]
    state["result"] = str(results[0])
    return state

def analyze_result(state: State) -> State:
    """Analyze if we have enough information to answer the query"""
    print("analyzing the result...")
    messages = [SystemMessage(content="""
    You are an expert in analyzing search results.
    Your task is to determine if the search result contains at least 10000 words to answer the user's query.
    
    Return "yes" if the result contains at least 10000 words.
    Return "no" if the result does not contain at least 10000 words.
    """), HumanMessage(content=f"query: {state['query']}\nresult: {state['result']}")]
    response = llm.invoke(messages).content
    print(f"analysis: {response}")
    if "yes" in response:
        state["need_more_info"] = False
    else:
        state["need_more_info"] = True
    return state


def deep_search(state: State) -> State:
    """Deep search for more information"""
    print("deep searching...")
    detailed_query = f"detailed information about: {state['query']}"
    response = tavily_client.search(query=detailed_query, max_results=3)
    results = [{"title": result["title"], "url": result["url"], "content": result["content"]} for result in response["results"]]
    state["result"] = str(results[0])
    state["need_more_info"] = False
    return state

def generate_final_answer(state: State) -> State:
    """Generate the final answer"""
    print("generating final answer...")
    messages = [SystemMessage(content="You are a good summarizer, summarize the text"), HumanMessage(content=state["result"])]
    state["final_answer"] = llm.invoke(messages).content
    return state

def should_deep_search(state: State) -> str:
    """Decide if we need to deep search"""
    return "deep_search" if state["need_more_info"] else "generate_final_answer"

workflow = StateGraph(State)

workflow.add_node("search_web", search_web)
workflow.add_node("analyze_result", analyze_result)
workflow.add_node("deep_search", deep_search)
workflow.add_node("generate_final_answer", generate_final_answer)

workflow.add_edge(START, "search_web")
workflow.add_edge("search_web", "analyze_result")
workflow.add_conditional_edges(
    "analyze_result",
    should_deep_search,
    {"deep_search": "deep_search", "generate_final_answer": "generate_final_answer"}
)
workflow.add_edge("deep_search", "generate_final_answer")
workflow.add_edge("generate_final_answer", END)

app = workflow.compile()

result = app.invoke({"query": "How do transformers work in machine learning?", "result":"", "analysis":"", "need_more_info":False, "final_answer":""})
print(result["final_answer"])