"""AG-UI server example."""

import os
from typing_extensions import Annotated
from pydantic import Field
import uvicorn
from agent_framework import Agent
from agent_framework_foundry import FoundryChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.identity import AzureCliCredential
from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()  # .env 파일 로드

# Read required configuration
endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
deployment_name = os.environ.get("FOUNDRY_MODEL")

if not endpoint:
    raise ValueError("⚠️ FOUNDRY_PROJECT_ENDPOINT 환경 변수가 필요합니다")
if not deployment_name:
    raise ValueError("⚠️ FOUNDRY_MODEL 환경 변수가 필요합니다")

chat_client = FoundryChatClient(
    credential=AzureCliCredential(),
    project_endpoint=endpoint,
    model=deployment_name,
)

# Create the AI agent
agent = Agent(
    name="AGUIAssistant",
    instructions="🤖 당신은 도움이 되는 어시스턴트입니다.",
    client=chat_client,
)

# 날씨 정보를 제공하는 도구 함수 정의
def get_weather(
    location: Annotated[str, Field(description="☀️ 날씨를 조회할 위치입니다.")],
) -> str:
    """특정 위치의 날씨 정보를 조회합니다."""
    return f"☁️ {location}의 날씨는 흐림이며 최고 기온은 15°C입니다."

# 날씨 정보를 제공하는 Agent 생성
weather_agent = Agent(
    name="AGUIAssistant",
    instructions="🤖 당신은 도움이 되는 어시스턴트입니다.",
    client=chat_client,
    tools=[get_weather]
)

# Create FastAPI app
app = FastAPI(title="AG-UI Server")

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")
add_agent_framework_fastapi_endpoint(app, weather_agent, "/weather")

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8888)