import asyncio
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential

async def basic_foundry_mcp_example():
    """Hosted MCP 도구를 사용하는 Foundry 에이전트의 기본 예시"""
    async with AzureCliCredential() as credential:
        client = FoundryChatClient(credential=credential)
        # client.get_mcp_tool() 메서드를 사용하여
        # Foundry에서 호스팅되는 MCP 도구를 생성할 수 있습니다.
        learn_mcp = client.get_mcp_tool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
        )

        # Hosted MCP 도구를 사용하는 에이전트를 생성합니다.
        async with Agent(
            client=client,
            name="MicrosoftLearnAgent",
            instructions="당신은 Microsoft Learn 관련 내용은 MCP를 활용해서 질문에 답변합니다."
                        +"MCP를 사용할 수 없는 질문은 모른다고 답변해야 합니다.",
            tools=[learn_mcp],
        ) as agent:
            # Simple query without approval workflow
            result = await agent.run(
                "롱블랙은 어떻게 만드나요?"
            )
            print(result.text)

if __name__ == "__main__":
    asyncio.run(basic_foundry_mcp_example())