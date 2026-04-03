import asyncio
import os
from agent_framework import Agent
from agent_framework_foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

async def multi_tool_mcp_example():
    """Hosted MCP 도구를 사용하는 Foundry 에이전트의 기본 예시"""
    async with AzureCliCredential() as credential:
        client = FoundryChatClient(credential=credential)
        # Create multiple MCP tools using the client method
        learn_mcp = client.get_mcp_tool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
            approval_mode="never", # 승인 없이 MCP 도구 자동 실행
        )
        github_mcp = client.get_mcp_tool(
            name="GitHub MCP",
            url="https://api.githubcopilot.com/mcp/",
            approval_mode="never",  # 승인이 필요하다면 "always_require" 설정
            headers={"Authorization": "Bearer <GITHUB_API_TOKEN>"}  # GitHub API 토큰,
        )

        # Create agent with multiple MCP tools
        async with Agent(
            client=client,
            name="MultiToolAgent",
            instructions="당신은 MS Learn 기술문서를 검색하여 정보를 제공하고, "
                        + "GitHub 저장소를 검색하여 정보를 제공합니다."
                        + "MCP를 사용할 수 없는 질문은 모른다고 답변해야 합니다.",
            tools=[learn_mcp, github_mcp],
        ) as agent:
            result = await agent.run(
                "내 깃헙의 리포들을 나열해 주세요"
            )
            print(result.text)

if __name__ == "__main__":
    asyncio.run(multi_tool_mcp_example())