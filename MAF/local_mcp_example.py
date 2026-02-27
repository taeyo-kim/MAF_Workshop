import asyncio
from agent_framework import Agent, MCPStdioTool
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

""" stdio로 로컬 MCP 서버를 사용하는 예제 """
load_dotenv()

async def local_mcp_example():
    async with (
        # 로컬 uvx mcp-server-calculator라는 MCP 서버를 MCPStdioTool로 연결합니다. 
        # 이 서버는 간단한 수학 계산을 수행하는 MCP 도구입니다.
        MCPStdioTool(
            name="calculator",
            command="uvx",
            args=["mcp-server-calculator"]
        ) as mcp_server,
        # 에이전트를 생성하며, mcp_server를 도구로 추가합니다. 
        # 또한, 에이전트는 Azure OpenAI Chat 모델을 사용하도록 설정되어 있습니다.
        Agent(
            client=AzureOpenAIChatClient(credential=AzureCliCredential()),
            name="MathAgent",
            instructions="당신은 유용한 수학 도우미입니다. 계산을 해결할 수 있습니다.",
            tools=mcp_server
        ) as agent,
    ):
        result = await agent.run("15 * 23 + 45은 무엇입니까?")
        print(result)

if __name__ == "__main__":
    asyncio.run(local_mcp_example())
