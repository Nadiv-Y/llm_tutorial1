from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
import sqlite3
import json



load_dotenv()

@tool
def query_tasks_db(query_type: str, user_name: str = None, status: str = None):
    """Query the tasks database

    Args:
        query_type: "all_tasks", "tasks_by_user", "tasks_by_status"
        user_name: Name of the user to query for
        status: Status of the tasks to query for

    Returns:
        str: JSON string of the query results
    """
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    if query_type == "all_tasks":
        cursor.execute("SELECT users.name, tasks.title, tasks.status FROM tasks JOIN users ON tasks.user_id = users.id")
    elif query_type == "tasks_by_user":
        cursor.execute("SELECT users.name, tasks.title, tasks.status FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.name LIKE ?", ("%" + user_name + "%",))
    elif query_type == "tasks_by_status":
        cursor.execute("SELECT users.name, tasks.title, tasks.status FROM tasks JOIN users ON tasks.user_id = users.id WHERE tasks.status LIKE ?", ("%" + status + "%",))
    results = [{"row" : i+1, "data" : row} for i, row in enumerate(cursor.fetchall())]
    conn.close()
    return json.dumps(results)



model = ChatOpenAI(model="gpt-4o-mini")

model_with_tools = model.bind_tools([query_tasks_db])

queries = [
    "Show me all tasks for Alice",
    "Show me all tasks with pending status",
    "Show me all tasks"
]

for query in queries:
    response = model_with_tools.invoke(query)
    if response.tool_calls:
        messages = [HumanMessage(content=query), response]
        for tool_call in response.tool_calls:
            function_name = tool_call["name"]
            function_args = tool_call["args"]
            print(function_name, function_args)
            result = globals()[function_name].invoke(function_args)
            print(result)
            messages.append(ToolMessage(tool_call_id=tool_call["id"], content=str(result)))
        final_response = model_with_tools.invoke(messages)
        print(final_response.content)