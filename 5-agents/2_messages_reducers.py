from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
import operator


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    system_message = SystemMessage(content="You are a poet, answer in a poem")
    full_messages = [system_message] + messages
    response = llm.invoke(full_messages)

    return {"messages": [response]}

workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

app = workflow.compile()

result = app.invoke({
    "messages": [HumanMessage(content="Hello, What is 2 + 2?")]
})
print(result["messages"][-1].content)