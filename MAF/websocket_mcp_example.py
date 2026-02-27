import asyncio
from agent_framework import Agent, MCPWebsocketTool
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

"""WebSocket 기반의 MCP 서버를 사용하는 예제입니다."""

async def websocket_mcp_example():

    async with (
        MCPWebsocketTool(
            name="restaurant-server",
            url="ws://localhost:8765",  # 실제 WebSocket MCP 서버 URL로 변경하세요
            load_prompts=False,         # 서버가 prompts/list를 지원하지 않으므로 비활성화
        ) as mcp_server,
        Agent(
            client=AzureOpenAIChatClient(credential=AzureCliCredential()),
            name="RestaurantAgent",
            instructions="당신은 레스토랑에서 서빙을 제공하는 에이전트입니다.",
            tools=mcp_server
        ) as agent,
    ):
        result = await agent.run("오늘의 스페셜 메뉴는 무엇입니까?")
        print(result)

if __name__ == "__main__":
    asyncio.run(websocket_mcp_example())