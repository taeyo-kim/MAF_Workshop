# Copyright (c) Microsoft. All rights reserved.
"""Foundry-based weather agent for Agent Framework Debug UI.

This agent uses Azure AI Foundry with Azure CLI authentication.
Make sure to run 'az login' before starting devui.
"""

import os
from pathlib import Path
from typing import Annotated

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field

from dotenv import load_dotenv
load_dotenv()  # .env 파일 로드

# NOTE: approval_mode="never_require" is for sample brevity. Use "always_require" in production; see samples/getting_started/tools/function_tool_with_approval.py and samples/getting_started/tools/function_tool_with_approval_and_threads.py.
def get_weather(
    location: Annotated[str, Field(description="날씨를 가져올 위치입니다. 📍")],
) -> str:
    """주어진 위치의 날씨를 가져옵니다. ☀️🌦️"""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    temperature = 22
    return f"The weather in {location} is {conditions[0]} with a high of {temperature}°C."

def get_forecast(
    location: Annotated[str, Field(description="예보를 가져올 위치입니다. 📍")],
    days: Annotated[int, Field(description="예보 기간(일) 📅")] = 3,
) -> str:
    """여러 날의 날씨 예보를 가져옵니다. 📊☁️"""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    forecast: list[str] = []

    for day in range(1, days + 1):
        condition = conditions[day % len(conditions)]
        temp = 18 + day
        forecast.append(f"Day {day}: {condition}, {temp}°C")

    return f"Weather forecast for {location}:\n" + "\n".join(forecast)


# Agent instance following Agent Framework conventions
agent = Agent(
    name="FoundryWeatherAgent",
    client=FoundryChatClient(
        credential=AzureCliCredential(),        
    ),
    instructions="""
    당신은 Azure AI Foundry 모델을 사용하는 날씨 어시스턴트입니다. ☀️🌦️ 
    모든 위치에 대한 현재 날씨 정보와 예보를 제공할 수 있습니다. 항상 도움이 되고 
    요청을 받으면 상세한 날씨 정보를 제공하세요. 💁✨
    """,
    tools=[get_weather, get_forecast],
)

def main():
    """Launch the Foundry weather agent in DevUI."""
    import logging

    from agent_framework.devui import serve

    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)

    logger.info("Starting Foundry Weather Agent")
    logger.info("Available at: http://localhost:8090")
    logger.info("Entity ID: agent_FoundryWeatherAgent")
    logger.info("Note: Make sure 'az login' has been run for authentication")

    # Launch server with the agent
    serve(entities=[agent], port=8090, auto_open=True)

    # result = await agent.run("What is the weather like in Amsterdam?")
    # print(result.text)

if __name__ == "__main__":
    main()
