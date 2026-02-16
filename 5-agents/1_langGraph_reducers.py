from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated
import operator

class State(TypedDict):
    counter: Annotated[int, operator.add]
    status: str

def increment(state: State) -> State:
    print(state)
    return {"counter": 1, "status": "incremented"}


workflow = StateGraph(State)
workflow.add_node("increment", increment)
workflow.add_edge(START, "increment")
workflow.add_edge("increment", END)

app = workflow.compile()

result = app.invoke({"counter": 1, "status": "initial"})
print(result)