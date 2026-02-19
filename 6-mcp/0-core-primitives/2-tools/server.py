from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tools-demo")

@mcp.tool()
def add(a: int, b: int):
    result = a + b
    return f"The result of adding {a} and {b} is {result}"

@mcp.tool()
def greet(name: str, formal: bool = False):
    if formal:
        return f"Hello, {name}, how are you?"
    else:
        return f"Hi, {name}, what's up?"

mcp.run(transport="stdio")