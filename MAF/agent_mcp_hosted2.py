import asyncio
import os
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agents.aio import AgentsClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

async def basic_foundry_mcp_example():
    """Hosted MCP 도구를 사용하는 Foundry 에이전트의 기본 예시"""
    
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(credential=credential) as client,
    ):
        # Create a hosted MCP tool using the client method
        learn_mcp = client.get_mcp_tool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
            approval_mode="never",  # 승인 없이 MCP 도구 자동 실행
        )

        github_mcp = client.get_mcp_tool(
            name="GitHub MCP", 
            url="https://api.githubcopilot.com/mcp",
            approval_mode="never",   # 승인이 필요하다면 "always_require" 설정
            headers={"Authorization": "Bearer {GITHUB_PAT}"},  
        )

        # 위에서 생성한 여러 MCP 도구를 등록할 수 있습니다.
        agent = client.as_agent(
            name="MultiToolAgent",
            instructions="당신은 MS Learn 기술문서와 GitHub 저장소를 검색하여 정보를 제공합니다."
                        +"MCP를 사용할 수 없는 질문은 모른다고 답변해야 합니다.",
            tools=[learn_mcp, github_mcp],
        )
        session = agent.create_session()
        
        # 질문
        result = await agent.run("내 깃헙의 리포들을 나열해 주세요", session=session)
        print(result)

if __name__ == "__main__":
    asyncio.run(basic_foundry_mcp_example())