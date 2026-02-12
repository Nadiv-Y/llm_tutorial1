from typing import Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from tavily import TavilyClient
from typing_extensions import TypedDict
from typing import Annotated
import operator
import os

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatOpenAI(model="gpt-4o-mini")

# class ReplaceState(TypedDict):
#     counter: int
#     status: str


# def increment(state: ReplaceState) -> ReplaceState:
#     """Increment the counter"""
#     return {
#         "counter": 1,
#         "status": "incremented"
#     }



# workflow = StateGraph(ReplaceState)

# workflow.add_node("increment", increment)

# workflow.add_edge(START, "increment")
# workflow.add_edge("increment", END)

# app = workflow.compile()

# result = app.invoke({"counter": 1, "status": ""})
# print(result)



# class AccumulateState(TypedDict):
#     counter: Annotated[int, operator.add]
#     status: str


# def accumulate(state: AccumulateState) -> AccumulateState:
#     """Accumulate the counter"""
#     return {
#         "counter": 1,
#         "status": "accumulated"
#     }

# workflow = StateGraph(AccumulateState)

# workflow.add_node("accumulate", accumulate)

# workflow.add_edge(START, "accumulate")
# workflow.add_edge("accumulate", END)

# app = workflow.compile()

# result = app.invoke({"counter": 1, "status": ""})
# print(result)


class ListState(TypedDict):
    items: Annotated[list, operator.add]
    total_items: int

def add_item(state: ListState) -> ListState:
    """Add an item to the list"""
    state["total_items"] = len(state["items"]) + 1
    state["items"] = ["This is the third item"]
    return state

workflow = StateGraph(ListState)

workflow.add_node("add_item", add_item)

workflow.add_edge(START, "add_item")
workflow.add_edge("add_item", END)

app = workflow.compile()

result = app.invoke({"items": ["This is the first item", "This is the second item"], "total_items": 32})
print(result)