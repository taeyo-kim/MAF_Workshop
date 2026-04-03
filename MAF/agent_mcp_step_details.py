import asyncio
import os
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

async def basic_foundry_mcp_example():
    """Hosted MCP 도구를 사용하는 Foundry 에이전트의 기본 예시"""
    
    async with AzureCliCredential() as credential:
        client = FoundryChatClient(credential=credential)

        # Create a hosted MCP tool using the client method
        learn_mcp = client.get_mcp_tool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
            approval_mode="never",  # 승인 없이 MCP 도구 자동 실행
        )

        # Create agent with hosted MCP tool
        agent = client.as_agent(
            name="MicrosoftLearnAgent", 
            instructions="당신은 Microsoft Learn 관련 내용은 MCP를 활용해서 질문에 답변합니다."
                        +"MCP를 사용할 수 없는 질문은 모른다고 답변해야 합니다.",
            tools=learn_mcp,
        )

        # Simple query without approval workflow
        session = agent.create_session()
        result = await agent.run(
            "Foundry Agent 문서에서 MCP 도구 호출과 관련된 내용을 요약해 주세요.",
            session=session,
        )

        # MCP 호출 이력 출력
        print("=" * 60)
        print("📋 MCP 호출 이력")
        print("=" * 60)
        mcp_call_count = 0

        # result.messages의 Content 타입으로 MCP 호출 추적
        tool_results: dict[str, str] = {}
        for msg in (result.messages or []):
            for content in (msg.contents or []):
                if content.type == "mcp_server_tool_result":
                    tool_results[content.call_id] = content.output or ""

        for msg in (result.messages or []):
            for content in (msg.contents or []):
                if content.type == "mcp_server_tool_call":
                    mcp_call_count += 1
                    output = tool_results.get(content.call_id, "")
                    print(f"\n[호출 #{mcp_call_count}]")
                    print(f"  서버   : {content.server_name or 'N/A'}")
                    print(f"  도구   : {content.tool_name}")
                    print(f"  인수   : {content.arguments}")
                    print(f"  결과   : {str(output)[:300]}{'...' if len(str(output)) > 300 else ''}")
        if mcp_call_count == 0:
            print("  (MCP 호출 없음)")
        print("=" * 60)
        print("\n💬 최종 응답:")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(basic_foundry_mcp_example())