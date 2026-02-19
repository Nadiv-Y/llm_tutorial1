
import asyncio
import sys
from mcp.client.stdio  import stdio_client
from mcp import ClientSession, StdioServerParameters
from pathlib import Path

async def main():
    server_script = Path(__file__).parent / "server.py"
    
    server_params = StdioServerParameters(
        command=sys.executable  ,
        args=[str(server_script)]
    )

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            
            resources = await session.list_resources()
            
            
            for r in resources.resources:
                result = await session.read_resource(r.uri)
                content = result.contents[0].text
                print(content)
                

if __name__ == "__main__":
    asyncio.run(main())