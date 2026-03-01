import asyncio
import os
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agents.aio import AgentsClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

async def basic_foundry_mcp_example():
    """Basic example of Foundry agent with hosted MCP tools."""
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
            "Azure AI Agent 문서에서 MCP 도구 호출과 관련된 내용을 요약해 주세요.",
            session=session,
        )

        # MCP 호출 이력 출력
        print("=" * 60)
        print("📋 MCP 호출 이력")
        print("=" * 60)
        thread_id = session.service_session_id
        agents_client = client.agents_client
        mcp_call_count = 0
        runs = agents_client.runs.list(thread_id=thread_id)
        async for run in runs:
            steps = agents_client.run_steps.list(thread_id=thread_id, run_id=run.id)
            async for step in steps:
                if step.type == "tool_calls" and hasattr(step, "step_details"):
                    for tc in step.step_details.tool_calls:
                        if tc.type == "mcp":
                            mcp_call_count += 1
                            print(f"\n[호출 #{mcp_call_count}]")
                            print(f"  서버  : {tc.server_label}")
                            print(f"  도구  : {tc.name}")
                            print(f"  인수  : {tc.arguments}")
                            print(f"  결과  : {str(tc.output)[:300]}...")
        if mcp_call_count == 0:
            print("  (MCP 호출 없음)")
        print("=" * 60)
        print("\n💬 최종 응답:")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(basic_foundry_mcp_example())