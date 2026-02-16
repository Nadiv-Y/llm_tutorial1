from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
from langchain_openai import ChatOpenAI
import sqlite3
import json
from langchain_core.tools import tool


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
conn = sqlite3.connect(":memory:")  
cursor = conn.cursor()

cursor.execute("Create table sales(id integer primary key autoincrement, product varchar(255), quantity integer, price integer)")
cursor.execute("INSERT INTO sales (product, quantity, price) VALUES ('laptop', 5, 1000)")
cursor.execute("INSERT INTO sales (product, quantity, price) VALUES ('laptop', 30, 25)")
cursor.execute("INSERT INTO sales (product, quantity, price) VALUES ('Keyboard', 10, 75)")
conn.commit()


@tool
def get_sales(product: str) -> str:
    """Get the sales of a product"""
    cursor.execute("SELECT * FROM sales WHERE product = ?", (product,))
    rows = cursor.fetchall()
    print("rows")
    print(rows)
    formatted_rows = [{"id": row[0], "product": row[1], "quantity": row[2], "price": row[3]} for row in rows]
    return json.dumps(formatted_rows)

tools = [get_sales]

llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    system_message = SystemMessage(content="You are a sql agent. use tools to answer the question if needed")
    full_messages = [system_message] + messages
    response = llm_with_tools.invoke(full_messages)

    return {"messages": [response]}

def tool_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    last_message = messages[-1]
    print(last_message)
    tool_calls = last_message.tool_calls
    
    results = []
    for tool_call in tool_calls:
        function_name = tool_call["name"]
        function_args = tool_call["args"]
        print(function_name, function_args)
        observation = globals()[function_name].invoke(function_args)
        print("observation")
        print(observation)
        results.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
    return {"messages": results}

def should_continue(state: ChatState) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    print(last_message)
    if last_message.tool_calls:
        return "tools"
    else:
        return END

workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "chatbot")
workflow.add_conditional_edges(
    "chatbot",
    should_continue,
    ["tools", END]
)
workflow.add_edge("tools", "chatbot")


app = workflow.compile()

result = app.invoke({
    "messages": [HumanMessage(content="How many laptops did we sell?")]
})
print(result["messages"][-1].content)
