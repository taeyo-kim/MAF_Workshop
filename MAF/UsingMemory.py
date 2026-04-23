"""
Microsoft Agent Framework + Azure AI Foundry Memory 예제

요구 사항
---------
1. pip install agent-framework agent-framework-foundry azure-ai-projects azure-identity python-dotenv
2. .env 파일에 다음 값이 설정되어 있어야 합니다.
     FOUNDRY_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com/api/projects/<project-name>
     FOUNDRY_MODEL=<chat 모델 배포 이름, 예: gpt-4o-mini>
     FOUNDRY_EMBEDDING_MODEL=<임베딩 모델 배포 이름, 예: text-embedding-3-small>
3. 로컬에서는 `az login` 으로 Azure CLI 로그인을 미리 해두세요.

핵심 포인트
-----------
- `FoundryMemoryProvider`는 내부적으로 **비동기** `azure.ai.projects.aio.AIProjectClient`를
  사용합니다. 따라서 자격 증명도 `azure.identity.aio` 쪽을 써야 합니다.
- Memory Store는 미리 포털/SDK로 생성되어 있어야 하며, 없으면 이 스크립트가
  `MemoryStoreDefaultDefinition` 으로 새로 만듭니다.
- Memory Store를 사용하려면 `allow_preview=True` 옵션이 필요합니다(프리뷰 기능).
- 에이전트는 `FoundryChatClient.as_agent(...)` 로 생성하고,
  `context_providers=[memory_provider]` 로 메모리를 연결합니다.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from agent_framework import (
    AgentSession,
    ContextProvider,
    Message,
    SessionContext,
    SupportsAgentRun,
)
from agent_framework.foundry import FoundryChatClient, FoundryMemoryProvider
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    MemoryStoreDefaultDefinition,
    MemoryStoreDetails,
)
from azure.identity.aio import AzureCliCredential  # 로컬 개발용
# from azure.identity.aio import DefaultAzureCredential  # Hosted(Managed Identity) 권장

load_dotenv()

FOUNDRY_PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
CHAT_MODEL = os.environ["FOUNDRY_MODEL"]
EMBEDDING_MODEL = os.environ.get("FOUNDRY_EMBEDDING_MODEL", "text-embedding-3-small")

MEMORY_STORE_NAME = "my_memory_store"
USER_SCOPE = "user_123"  # 사용자 단위로 메모리 분리

# 로컬 파일 기반 사용자 메모리 저장 위치
LOCAL_MEMORY_FILE = Path(__file__).with_name("user_memory.json")


class LocalUserMemoryProvider(ContextProvider):
    """Foundry Memory 프리뷰 서비스가 mock 응답을 반환할 때를 대비한 로컬 백업 메모리.

    동작:
      - 파일(`LOCAL_MEMORY_FILE`)에 사용자 scope 별 과거 user/assistant 메시지를 저장.
      - 매 `before_run` 시 저장된 사실을 컨텍스트 메시지로 주입.
      - 매 `after_run` 시 새로 발생한 user/assistant 메시지를 추가 저장.

    Foundry Memory 가 정상 동작하면 `FoundryMemoryProvider` 와 자연스럽게 공존합니다.
    """

    def __init__(self, scope: str, file_path: Path = LOCAL_MEMORY_FILE) -> None:
        super().__init__(source_id="local_user_memory")
        self.scope = scope
        self.file_path = file_path

    # ---- 파일 IO 헬퍼 ----------------------------------------------------
    def _load_all(self) -> dict[str, list[dict[str, str]]]:
        if not self.file_path.exists():
            return {}
        try:
            return json.loads(self.file_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_all(self, data: dict[str, list[dict[str, str]]]) -> None:
        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _scope_messages(self) -> list[dict[str, str]]:
        return self._load_all().get(self.scope, [])

    def _append_messages(self, new_items: list[dict[str, str]]) -> None:
        data = self._load_all()
        bucket = data.setdefault(self.scope, [])
        bucket.extend(new_items)
        # 너무 길어지지 않도록 최근 200개만 유지
        if len(bucket) > 200:
            data[self.scope] = bucket[-200:]
        self._save_all(data)

    # ---- ContextProvider 훅 ---------------------------------------------
    async def before_run(
        self,
        *,
        agent: SupportsAgentRun,
        session: AgentSession,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        history = self._scope_messages()
        if not history:
            return
        # 사용자가 과거에 말한 정보만 모아서 한 덩어리로 주입
        user_facts = [m["content"] for m in history if m.get("role") == "user"]
        if not user_facts:
            return
        joined = "\n".join(f"- {fact}" for fact in user_facts[-30:])
        prompt = (
            "## 사용자가 과거 세션에서 직접 알려준 정보 (로컬 메모리)\n"
            "다음 사실들을 참고해 답변하세요.\n"
            f"{joined}"
        )
        context.extend_messages(
            self, [Message(role="user", contents=[prompt])]
        )

    async def after_run(
        self,
        *,
        agent: SupportsAgentRun,
        session: AgentSession,
        context: SessionContext,
        state: dict[str, Any],
    ) -> None:
        new_items: list[dict[str, str]] = []
        for msg in list(context.input_messages):
            if msg.role in {"user"} and msg.text and msg.text.strip():
                # 우리가 컨텍스트로 직접 주입한 메모리 프롬프트는 저장하지 않음
                if msg.text.lstrip().startswith("## 사용자가 과거 세션"):
                    continue
                new_items.append({"role": "user", "content": msg.text.strip()})
        if context.response and context.response.messages:
            for msg in context.response.messages:
                if msg.role == "assistant" and msg.text and msg.text.strip():
                    new_items.append({"role": "assistant", "content": msg.text.strip()})
        if new_items:
            self._append_messages(new_items)


async def ensure_memory_store(project_client: AIProjectClient) -> MemoryStoreDetails:
    """Memory Store가 없으면 기본 정의로 생성합니다."""
    try:
        return await project_client.beta.memory_stores.get(MEMORY_STORE_NAME)
    except Exception:
        print(f"[memory] '{MEMORY_STORE_NAME}' 이(가) 없어 새로 생성합니다...")
        return await project_client.beta.memory_stores.create(
            name=MEMORY_STORE_NAME,
            description="Memory store for my agent",
            definition=MemoryStoreDefaultDefinition(
                chat_model=CHAT_MODEL,
                embedding_model=EMBEDDING_MODEL,
            ),
        )


async def dump_existing_memories(project_client: AIProjectClient) -> None:
    """현재 메모리 저장소에 어떤 정보가 들어있는지 콘솔에 나열합니다.

    Foundry Memory 의 공식 API 에는 "list all memories" 엔드포인트가 없고,
    `search_memories` 만 제공됩니다. 따라서 두 가지 방식으로 조회합니다.
      1) items=None  → scope 전체에서 임의로 회수되는 메모리
      2) items=질의  → 사용자 식별/취향 관련 질문에 매칭되는 메모리
    """
    print("\n" + "=" * 60)
    print(f"[memory dump] store='{MEMORY_STORE_NAME}', scope='{USER_SCOPE}'")
    print("=" * 60)

    queries: list[tuple[str, list[dict] | None]] = [
        ("(1) scope 전체 (items=None)", None),
        (
            "(2) 사용자 식별 / 취향 질의",
            [{"role": "user", "type": "message",
              "content": "내 이름이 뭐고, 좋아하는 음식이 뭐야?"}],
        ),
    ]

    for label, items in queries:
        try:
            res = await project_client.beta.memory_stores.search_memories(
                name=MEMORY_STORE_NAME,
                scope=USER_SCOPE,
                items=items,
            )
        except Exception as e:
            print(f"\n{label}: 조회 실패 → {e}")
            continue

        memories = list(res.memories)
        print(f"\n{label}: {len(memories)}건")
        for i, m in enumerate(memories, start=1):
            content = (m.memory_item.content or "").strip()
            kind = type(m.memory_item).__name__
            print(f"  [{i}] ({kind}) {content}")

        # 모든 결과가 서비스 측 샘플 응답이면 경고
        contents = [(m.memory_item.content or "").lower() for m in memories]
        if contents and all("sample memory content" in c for c in contents):
            print("  ⚠ 모두 Foundry Memory 프리뷰 서비스의 샘플 응답입니다."
                  " 실제 사용자 메모리가 저장/조회되지 않은 상태입니다.")

    print("=" * 60)


async def main() -> None:
    # (1) 비동기 자격증명 + 비동기 AIProjectClient
    async with AzureCliCredential() as credential, AIProjectClient(
        endpoint=FOUNDRY_PROJECT_ENDPOINT,
        credential=credential,
        allow_preview=True,  # memory_stores 는 preview 기능
    ) as project_client:

        # (2) Memory Store 확보 (없으면 생성)
        store = await ensure_memory_store(project_client)
        print(f"[memory] memory store ready: {store.name}")

        # (2-b) ★ 기존 저장소 상태 점검 – 이전 실행에서 저장된 메모리가 실제로
        #         남아있는지 콘솔에 먼저 나열한다.
        await dump_existing_memories(project_client)

        # (3) FoundryChatClient 생성 (FOUNDRY_MODEL 환경변수 자동 사용)
        chat_client = FoundryChatClient(project_client=project_client)

        # (4) Provider 들 생성
        # ----------------------------------------------------------------
        # FoundryMemoryProvider: Foundry Memory 서비스(현재 프리뷰)에 저장/검색.
        #   - 현재 환경에서는 서비스가 mock 응답을 돌려주는 알려진 이슈가 있어
        #     실제 사용자 정보가 새 세션에 반영되지 않습니다.
        # LocalUserMemoryProvider: 위 이슈를 보완하는 로컬 파일 기반 메모리.
        #   - user_memory.json 파일에 사용자 발화/응답을 누적 저장하고,
        #     매 호출마다 컨텍스트로 주입해서 새 세션에서도 기억이 유지되게 합니다.
        # ----------------------------------------------------------------
        memory_provider = FoundryMemoryProvider(
            project_client=project_client,
            memory_store_name=MEMORY_STORE_NAME,
            scope=USER_SCOPE,
            update_delay=0,  # 0 이면 즉시 메모리 업데이트
        )
        local_memory_provider = LocalUserMemoryProvider(scope=USER_SCOPE)

        # 로컬 메모리 현재 상태 표시
        local_history = local_memory_provider._scope_messages()
        print(f"\n[local memory] '{LOCAL_MEMORY_FILE.name}' scope='{USER_SCOPE}' "
              f"메시지 {len(local_history)}건 적재됨")
        for i, m in enumerate(local_history[-10:], start=1):
            print(f"  [{i}] ({m['role']}) {m['content'][:80]}")

        # (5) 에이전트 생성 – 두 Provider 모두 등록
        agent = chat_client.as_agent(
            name="MyAgentWithMemory",
            instructions=(
                "당신은 사용자의 취향과 개인정보를 장기 기억으로 관리하는 친절한 비서입니다. "
                "이전 대화에서 얻은 메모리가 있다면 자연스럽게 활용해 답변하세요."
            ),
            context_providers=[memory_provider, local_memory_provider],
        )

        
        session1 = agent.create_session()

        r0 = await agent.run(
            "혹시 내 이름과 음식 취향 기억해?",
            session=session1,
        )
        print("\n[turn 1]", r0.text)

        r1 = await agent.run(
            "내 이름은 마이클이고, 채식 위주 한식을 좋아해. 이걸 기억해 줘.",
            session=session1,
        )
        print("\n[turn 2]", r1.text)

        r2 = await agent.run("내 이름과 음식 취향 기억해?", session=session1)
        print("\n[turn 3]", r2.text)


if __name__ == "__main__":
    asyncio.run(main())