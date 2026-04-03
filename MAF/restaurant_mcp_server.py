
from typing import Annotated
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from mcp.server.websocket import websocket_server
import uvicorn
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 오늘의 스페셜 메뉴를 반환하는 도구
def get_specials() -> Annotated[str, "🍽️ 메뉴에서 스페셜 항목을 반환합니다."]:
    return '''
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        '''

# 메뉴 아이템의 가격을 반환하는 도구
def get_item_price(
    menu_item: Annotated[str, "💰 메뉴 항목의 이름입니다."],
) -> Annotated[str, "메뉴 항목의 가격을 반환합니다."]:
    return "$9.99"

# RestaurantAgent 에이전트 생성 및 도구 제공
agent = FoundryChatClient(credential=AzureCliCredential()).as_agent(
    name="RestaurantAgent",
    instructions="🍴당신은 메뉴에 대한 질문에 답변하는 레스토랑 에이전트입니다.",
    tools=[get_specials, get_item_price],
)

# 에이전트를 MCP 서버로 전환
server = agent.as_mcp_server()

async def mcp_asgi(scope, receive, send):
    if scope["type"] == "websocket":
        async with websocket_server(scope, receive, send) as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    print("🍴 Restaurant MCP 서버 시작: ws://localhost:8765")
    uvicorn.run(mcp_asgi, host="127.0.0.1", port=8765)
