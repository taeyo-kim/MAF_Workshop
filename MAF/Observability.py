import asyncio
from agent_framework import Agent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from agent_framework.observability import configure_otel_providers
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk._logs.export import ConsoleLogRecordExporter 
from dotenv import load_dotenv

# Console에 trace와 log를 출력하도록 설정
# 동시에 환경변수에 지정된 OTEL_EXPORTER_OTLP_ENDPOINT로도 전송됨 (Aspire Dashboard)
configure_otel_providers(
    exporters=[
        ConsoleSpanExporter(),        # Trace를 콘솔에 출력
        ConsoleLogRecordExporter()    # Log를 콘솔에 출력
    ]
)

load_dotenv()  # .env 파일 로드

# Create the agent - telemetry is automatically enabled
agent = Agent(
    client=AzureOpenAIChatClient(credential=AzureCliCredential()),
    name="Joker",
    instructions="당신은 한국어로 농담을 잘하는 유쾌한 코미디언입니다. 😄🎭"
)

# Run the agent
async def main() -> None:
    result = await agent.run("로봇에 대한 농담 하나 들려줘. 🤖")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
