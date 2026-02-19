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
            
            prompts = await session.list_prompts()

            print(prompts)
            
            
            result = await session.get_prompt("translate_to_hebrew", arguments={"text": "Hello, World!"})
            print("dhfkhfbeufheuhwu")
            print(result)
                

asyncio.run(main())