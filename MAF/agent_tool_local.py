import asyncio
from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

async def basic_foundry_mcp_example():
    """Basic example of Foundry agent with hosted MCP tools."""
    async with (
        AzureCliCredential() as credential,
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
        ) as mcp_tool,
        Agent(
            client=AzureAIAgentClient(credential=credential),
            name="MicrosoftLearnAgent",
            instructions="당신은 Microsoft Learn 관련 내용은 MCP를 활용해서 질문에 답변합니다. MCP를 사용할 수 없는 질문은 모른다고 답변해야 합니다.",
            tools=mcp_tool,
        ) as agent,
    ):
        # 첫 번째 질문
        result = await agent.run("롱블랙이란 무엇인가요?")
        print(result)

        print("\n" + "=" * 60 + "\n")

        # 두 번째 질문
        result = await agent.run("Azure AI Search의 주요 기능은 무엇인가요?")
        print(result)

if __name__ == "__main__":
    asyncio.run(basic_foundry_mcp_example())