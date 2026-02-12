from typing import Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from tavily import TavilyClient
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
import operator
import os

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatOpenAI(model="gpt-4o-mini")

# class ChatState(TypedDict):
#     messages: Annotated[list,add_messages]

# def chatbot(state: ChatState) -> ChatState:
#     """Chatbot"""
#     messages = state["messages"]
#     system_message = SystemMessage(content="You are a helpful assistant")
#     full_messages = [system_message] + messages
#     response = llm.invoke(full_messages)
#     state["messages"] = [response]
#     return state

# workflow = StateGraph(ChatState)

# workflow.add_node("chatbot", chatbot)

# workflow.add_edge(START, "chatbot")
# workflow.add_edge("chatbot", END)

# app = workflow.compile()

# result = app.invoke({"messages": [HumanMessage(content="Hello")]})
# print(result["messages"])


class ConversationState(TypedDict):
    messages: Annotated[list,add_messages]
    user_name: str

def contextual_chatbot(state: ConversationState) -> ConversationState:
    """Chatbot"""
    messages = state["messages"]
    user_name = state["user_name"]
    system_message = SystemMessage(content=f"you are a helpful assistant talking to {user_name}, be friendly")
    full_messages = [system_message] + messages
    response = llm.invoke(full_messages)
    state["messages"] = [response]
    return state

contextual_workflow = StateGraph(ConversationState)

contextual_workflow.add_node("chatbot", contextual_chatbot)

contextual_workflow.add_edge(START, "chatbot")
contextual_workflow.add_edge("chatbot", END)

contextual_app = contextual_workflow.compile()

state = {"messages": [HumanMessage(content="Hi, my favorite color is blue")], "user_name": "John"}

result = contextual_app.invoke(state)
print(result["messages"])


state = {"messages": result["messages"] + [HumanMessage(content="What is my favorite color?")], "user_name": "John"}

result = contextual_app.invoke(state)
print(result["messages"])
