"""AG-UI server example."""

import os
import uvicorn
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
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

# Create FastAPI app
app = FastAPI(title="AG-UI Server")

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8888)