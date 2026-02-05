"""AG-UI server example."""

import os
import uvicorn
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.identity import AzureCliCredential
from fastapi import FastAPI

# Read required configuration
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

if not endpoint:
    raise ValueError("⚠️ AZURE_OPENAI_ENDPOINT 환경 변수가 필요합니다")
if not deployment_name:
    raise ValueError("⚠️ AZURE_OPENAI_CHAT_DEPLOYMENT_NAME 환경 변수가 필요합니다")

chat_client = AzureOpenAIChatClient(
    credential=AzureCliCredential(),
    endpoint=endpoint,
    deployment_name=deployment_name,
)

# Create the AI agent
agent = ChatAgent(
    name="AGUIAssistant",
    instructions="🤖 당신은 도움이 되는 어시스턴트입니다.",
    chat_client=chat_client,
)

# Create FastAPI app
app = FastAPI(title="AG-UI Server")

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8888)