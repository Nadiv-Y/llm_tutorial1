from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
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

class EmailAgentState(TypedDict):
    messages: Annotated[list, add_messages]
    email_to: str
    email_from: str
    email_subject: str
    email_body: str
    approved: bool

def draft_email(state: EmailAgentState) -> EmailAgentState:
    messages = state["messages"]
    system_message = SystemMessage(content="You are an email agent, based on the user request, extract the email to, from, subject and body, format it as json, like this: {\"email_to\": \"yossi@example.com\", \"email_from\": \"yossi@example.com\", \"email_subject\": \"Hello\", \"email_body\": \"Hello, how are you?\"}")
    full_messages = [system_message] + messages
    response = llm.invoke(full_messages)
    json_response = json.loads(response.content)
    return {"messages": [response], "email_to": json_response["email_to"], "email_from": json_response["email_from"], "email_subject": json_response["email_subject"], "email_body": json_response["email_body"], "approved": False}


def send_email(state: EmailAgentState) -> EmailAgentState:
    return {"messages": [AIMessage(content="Email sent to " + state["email_to"] + " with subject " + state["email_subject"])]}


workflow = StateGraph(EmailAgentState)
workflow.add_node("draft_email", draft_email)
workflow.add_node("send_email", send_email)
workflow.add_edge(START, "draft_email")
workflow.add_edge("draft_email", "send_email")
workflow.add_edge("send_email", END)

memory_saver = MemorySaver()

app = workflow.compile(checkpointer=memory_saver, interrupt_before=["send_email"])

user_input = input("Enter your request: (or 'exit' to quit): ")
config = {"configurable": {"thread_id": "thread_1"}}
app.invoke({"messages": [HumanMessage(content=user_input)], "email_to": "", "email_from": "", "email_subject": "", "email_body": "", "approved": False}, config=config)

while user_input != "exit":
    current_state = app.get_state(config)

    if not current_state.next:
        break

    values = current_state.values

    print("to: " + values["email_to"])
    print("from: " + values["email_from"])
    print("subject: " + values["email_subject"])
    print("body: " + values["email_body"])

    print("- ok -> approve the email")
    print("- to -> change the recipient")
    print("- from -> change the sender")
    print("- subject -> change the subject")
    print("- body -> change the body")
    print("- exit -> exit the loop")

    user_input = input("Enter your choice: ")

    if user_input == "exit":
        break
    elif user_input == "ok":
        app.update_state(config=config, values={"approved": True})
        app.invoke(None, config=config)
    elif user_input == "to":
        user_input = input("Enter the new recipient: ")
        app.update_state(config=config, values={"email_to": user_input})
    elif user_input == "from":
        user_input = input("Enter the new sender: ")
        app.update_state(config=config, values={"email_from": user_input})
    elif user_input == "subject":
        user_input = input("Enter the new subject: ")
        app.update_state(config=config, values={"email_subject": user_input})
    elif user_input == "body":
        user_input = input("Enter the new body: ")
        app.update_state(config=config, values={"email_body": user_input})

print(app.get_state(config).values['messages'][-1].content)