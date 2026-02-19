from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
import operator
import sqlite3
import json
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    system_message = SystemMessage(content="You are a helpful assistant")
    full_messages = [system_message] + messages
    response = llm.invoke(full_messages)

    return {"messages": [response]}

workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)


memory_saver = MemorySaver()

app = workflow.compile(checkpointer=memory_saver)

config = {"configurable": {"thread_id": "thread_1"}}

result = app.invoke({"messages": [HumanMessage(content="my name is Yossi and I live in Tel Aviv")]}, config=config)
print(result["messages"][-1].content)

result = app.invoke({"messages": [HumanMessage(content="where does Yossi live?")]}, config={"configurable": {"thread_id": "thread_2"}})
print(result["messages"][-1].content)

result = app.invoke({"messages": [HumanMessage(content="what is my name?")]}, config=config)
print(result["messages"][-1].content)
