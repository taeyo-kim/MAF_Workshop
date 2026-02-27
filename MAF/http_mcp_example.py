import asyncio
from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

"""HTTP 기반의 MCP 서버를 사용하는 예제입니다."""

async def http_mcp_example():
    
    async with (
        AzureCliCredential() as credential,
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
        ) as mcp_server,
        Agent(
            client=AzureAIAgentClient(credential=credential),
            name="DocsAgent",
            instructions="당신은 Microsoft Learn에 관한 질문에 도움을 주는 에이전트입니다.",
        ) as agent,
    ):
        result = await agent.run("Azure 스토리지 계정을 az cli를 사용하여 생성하는 방법은 무엇입니까?")
        print(result)

if __name__ == "__main__":
    asyncio.run(http_mcp_example())