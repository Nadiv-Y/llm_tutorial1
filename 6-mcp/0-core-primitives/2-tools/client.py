import asyncio
import sys
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from pathlib import Path

async def main():
    server_script = Path(__file__).parent / "server.py"
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_script)]
    )

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            
            tools = await session.list_tools()

            print(tools)
            
            
            result = await session.call_tool("add", arguments={"a": 1, "b": 2})
            print(result)

            result = await session.call_tool("greet", arguments={"name": "John", "formal": False})
            print(result)
                


asyncio.run(main())