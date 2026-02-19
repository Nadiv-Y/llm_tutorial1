from mcp.server.fastmcp import FastMCP

mcp = FastMCP("prompts-demo")

@mcp.prompt()
def translate_to_hebrew(text: str):
    """Translate the following text to Hebrew"""
    return f"Translate the following text to Hebrew: {text}"

mcp.run(transport="stdio")