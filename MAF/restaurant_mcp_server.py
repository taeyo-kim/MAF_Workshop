
from typing import Annotated
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from mcp.server.stdio import stdio_server
import anyio
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 오늘의 스페셜 메뉴를 반환하는 도구
def get_specials() -> Annotated[str, "Returns the specials from the menu."]:
    return '''
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        '''

# 메뉴 아이템의 가격을 반환하는 도구
def get_item_price(
    menu_item: Annotated[str, "The name of the menu item."],
) -> Annotated[str, "Returns the price of the menu item."]:
    return "$9.99"

# RestaurantAgent 에이전트 생성 및 도구 제공
agent = AzureOpenAIChatClient(credential=AzureCliCredential()).as_agent(
    name="RestaurantAgent",
    instructions="Answer questions about the menu.",
    tools=[get_specials, get_item_price],
)

# 에이전트를 MCP 서버로 전환
server = agent.as_mcp_server()

async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    anyio.run(run)
