from mcp.server.fastmcp import FastMCP

mcp = FastMCP("resources-demo")

@mcp.resource("greeting://hello")
def hello():
    return "Hello, World!"

@mcp.resource("greeting://dhdsbhsbhfjkh")
def hello():
    return "Hello, dfsffsfffs!"

mcp.run(transport="stdio")