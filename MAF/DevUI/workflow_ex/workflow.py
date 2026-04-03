# Copyright (c) Microsoft. All rights reserved.

"""Agent Workflow - Content Review with Quality Routing.

This sample demonstrates:
- Using agents directly as executors
- Conditional routing based on structured outputs
- Quality-based workflow paths with convergence

Use case: Content creation with automated review.
Writer creates content, Reviewer evaluates quality:
  - High quality (score >= 80): → Publisher → Summarizer
  - Low quality (score < 80): → Editor → Publisher → Summarizer
Both paths converge at Summarizer for final report.
"""

import os
from typing import Any

from agent_framework import AgentExecutorResponse, WorkflowBuilder
from agent_framework.foundry import FoundryChatClient
from pydantic import BaseModel
from azure.identity.aio import DefaultAzureCredential

from dotenv import load_dotenv
load_dotenv()  # .env 파일 로드

# Define structured output for review results
class ReviewResult(BaseModel):
    """점수와 피드백을 포함한 리뷰 평가 결과입니다. 📊👀"""

    score: int  # Overall quality score (0-100)
    feedback: str  # Concise, actionable feedback
    clarity: int  # Clarity score (0-100)
    completeness: int  # Completeness score (0-100)
    accuracy: int  # Accuracy score (0-100)
    structure: int  # Structure score (0-100)


# Condition function: route to editor if score < 80
def needs_editing(message: Any) -> bool:
    """리뷰 점수에 따라 콘텐츠가 편집이 필요한지 확인합니다. ✍️🚨"""
    if not isinstance(message, AgentExecutorResponse):
        return False
    try:
        review = ReviewResult.model_validate_json(message.agent_response.text)
        return review.score < 80
    except Exception:
        return False


# Condition function: content is approved (score >= 80)
def is_approved(message: Any) -> bool:
    """콘텐츠가 승인되었는지(고품질) 확인합니다. ✅✨"""
    if not isinstance(message, AgentExecutorResponse):
        return True
    try:
        review = ReviewResult.model_validate_json(message.agent_response.text)
        return review.score >= 80
    except Exception:
        return True


# Create Azure OpenAI chat client
chat_client = FoundryChatClient(credential=DefaultAzureCredential())

# Create Writer agent - generates content
writer = chat_client.as_agent(
    name="Writer",
    instructions=(
        "당신은 훌륭한 콘텐츠 작성자입니다. ✍️✨ "
        "사용자의 요청에 따라 명확하고 매력적인 콘텐츠를 만드세요. "
        "명확성, 정확성, 적절한 구조에 중점을 두세요."
    ),
)

# Create Reviewer agent - evaluates and provides structured feedback
reviewer = chat_client.as_agent(
    name="Reviewer",
    instructions=(
        "당신은 전문 콘텐츠 리뷰어입니다. 👀📊 "
        "작성자의 콘텐츠를 다음 기준으로 평가하세요:\n"
        "1. 명확성 - 이해하기 쉬운가요?\n"
        "2. 완성도 - 주제를 완전히 다루고 있나요?\n"
        "3. 정확성 - 정보가 정확한가요?\n"
        "4. 구조 - 잘 정리되어 있나요?\n\n"
        "다음을 포함하는 JSON 객체를 반환하세요:\n"
        "- score: 전체 품질 (0-100)\n"
        "- feedback: 간결하고 실행 가능한 피드백\n"
        "- clarity, completeness, accuracy, structure: 각 항목별 점수 (0-100)"
    ),
    default_options={"response_format": ReviewResult},
)

# Create Editor agent - improves content based on feedback
editor = chat_client.as_agent(
    name="Editor",
    instructions=(
        "당신은 숙련된 편집자입니다. ✍️🔧 "
        "리뷰 피드백과 함께 콘텐츠를 받게 됩니다. "
        "피드백에서 언급된 모든 문제를 해결하여 콘텐츠를 개선하세요. "
        "명확성, 완성도, 정확성, 구조를 향상시키면서 원래의 의도를 유지하세요."
    ),
)

# Create Publisher agent - formats content for publication
publisher = chat_client.as_agent(
    name="Publisher",
    instructions=(
        "당신은 발행 에이전트입니다. 📝✨ "
        "승인된 콘텐츠 또는 편집된 콘텐츠를 받습니다. "
        "적절한 제목과 구조로 발행용으로 포맷팅하세요."
    ),
)

# Create Summarizer agent - creates final publication report
summarizer = chat_client.as_agent(
    name="Summarizer",
    instructions=(
        "당신은 요약 에이전트입니다. 📊📝 "
        "다음을 포함하는 최종 발행 보고서를 작성하세요:\n"
        "1. 발행된 콘텐츠의 간략한 요약\n"
        "2. 사용된 워크플로우 경로(직접 승인 또는 편집)\n"
        "3. 주요 하이라이트와 시사점\n"
        "간결하고 전문적으로 작성하세요."
    ),
)

# Build workflow with branching and convergence:
# Writer → Reviewer → [branches]:
#   - If score >= 80: → Publisher → Summarizer (direct approval path)
#   - If score < 80: → Editor → Publisher → Summarizer (improvement path)
# Both paths converge at Summarizer for final report
builder = WorkflowBuilder(
    start_executor=writer,
    name="Content Review Workflow",
    description="Multi-agent content creation workflow with quality-based routing (Writer → Reviewer → Editor/Publisher)",
)

workflow = (
    builder
    .add_edge(writer, reviewer)
    # Branch 1: High quality (>= 80) goes directly to publisher
    .add_edge(reviewer, publisher, condition=is_approved)
    # Branch 2: Low quality (< 80) goes to editor first, then publisher
    .add_edge(reviewer, editor, condition=needs_editing)
    .add_edge(editor, publisher)
    # Both paths converge: Publisher → Summarizer
    .add_edge(publisher, summarizer)
    .build()
)


def main():
    """Launch the branching workflow in DevUI."""
    import logging

    from agent_framework.devui import serve

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)

    logger.info("Starting Agent Workflow (Content Review with Quality Routing)")
    logger.info("Available at: http://localhost:8093")
    logger.info("\nThis workflow demonstrates:")
    logger.info("- Conditional routing based on structured outputs")
    logger.info("- Path 1 (score >= 80): Reviewer → Publisher → Summarizer")
    logger.info("- Path 2 (score < 80): Reviewer → Editor → Publisher → Summarizer")
    logger.info("- Both paths converge at Summarizer for final report")

    serve(entities=[workflow], port=8093, auto_open=True)

if __name__ == "__main__":
    main()
