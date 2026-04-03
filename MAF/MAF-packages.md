# 📦 MAF 핵심 라이브러리 역할

Microsoft Agent Framework(MAF)는 여러 패키지로 구성된 계층적 의존성 구조를 가집니다.

> **1.0.0 GA 기준** (2026-04-02 릴리즈) — **`agent-framework-azure-ai`가 `agent-framework-openai`와 `agent-framework-foundry`로 분리**된 것이 가장 큰 변경 사항입니다.

---

## 📋 라이브러리 역할 요약

### GA(Stable) 패키지

| 라이브러리 | 계층 | 역할 |
|-----------|------|------|
| `agent-framework` | 최상위 메타 패키지 | `agent-framework-core[all]`을 설치하는 **umbrella 패키지**. 실제 코드는 없고, 모든 통합 패키지를 한 번에 설치하는 편의 패키지 |
| `agent-framework-core` | 핵심 엔진 | 에이전트·워크플로우·실행기(Executor)·이벤트 등 **플랫폼 독립적인 핵심 추상화** 제공. `[all]` extras로 모든 통합 패키지 설치 가능 |
| `agent-framework-openai` | LLM 클라이언트 | OpenAI 및 Azure OpenAI 연결 클라이언트 제공. `OpenAIChatClient`(Responses API), `OpenAIChatCompletionClient`(Chat Completions API), `OpenAIEmbeddingClient` 포함 |
| `agent-framework-foundry` | Azure Foundry 통합 | Azure AI Foundry 연결 클라이언트·사전 구성된 에이전트·임베딩 클라이언트·메모리 프로바이더 제공. `azure-ai-projects 2.x`에 의존 |

### Preview(Beta) 패키지

| 라이브러리 | 역할 |
|-----------|------|
| `agent-framework-orchestrations` | SequentialBuilder, ConcurrentBuilder, HandoffBuilder, GroupChatBuilder, MagenticBuilder 등 **멀티 에이전트 오케스트레이션 패턴** |
| `agent-framework-anthropic` | Anthropic Claude 모델 통합 |
| `agent-framework-claude` | Claude 에이전트 SDK 통합 |
| `agent-framework-bedrock` | AWS Bedrock 통합 |
| `agent-framework-foundry-local` | Foundry 로컬 실행 환경 통합 |
| `agent-framework-azure-cosmos` | Azure Cosmos DB 메모리/스토리지 통합 |
| `agent-framework-a2a` | Agent-to-Agent(A2A) 프로토콜 통신 |
| `agent-framework-ag-ui` | AG-UI 프로토콜 통합 |
| `agent-framework-redis` | Redis 기반 외부 스토리지/세션 통합 |
| `agent-framework-copilotstudio` | Microsoft Copilot Studio 통합 |
| `agent-framework-devui` | 개발용 UI (Dev UI) |
| 그 외 | `azure-ai-search`, `azurefunctions`, `chatkit`, `declarative`, `durabletask`, `github-copilot`, `lab`, `mem0`, `ollama`, `purview` 등 |

---

## 🗂️ 의존 관계 흐름

```
agent-framework 1.0.0  (메타 패키지 → agent-framework-core[all] 설치)
    └── agent-framework-core 1.0.0  (핵심 엔진 + [all] extras로 아래 패키지 모두 포함)
            ├── agent-framework-openai 1.0.0     ← OpenAI / Azure OpenAI 클라이언트
            │       └── openai
            ├── agent-framework-foundry 1.0.0    ← Azure AI Foundry 통합
            │       ├── agent-framework-openai
            │       ├── azure-ai-inference
            │       └── azure-ai-projects 2.x    ← Azure Foundry SDK (Microsoft 공식)
            ├── agent-framework-orchestrations   ← 멀티 에이전트 오케스트레이션 (beta)
            ├── agent-framework-anthropic        ← Anthropic Claude (beta)
            ├── agent-framework-bedrock          ← AWS Bedrock (beta)
            └── ... (기타 통합 패키지들)
```


> **구버전(`agent-framework-azure-ai`)과의 비교**: 1.0.0 GA에서 `agent-framework-azure-ai`가 역할에 따라 두 패키지로 분리되었습니다.
> - OpenAI / Azure OpenAI 클라이언트 → `agent-framework-openai`
> - Azure AI Foundry 통합 → `agent-framework-foundry`

---

## 🔍 각 라이브러리 상세 설명

### 1️⃣ `agent-framework` — 메타 패키지

- 실제 코드를 포함하지 않는 **umbrella 패키지**
- 내부적으로 `agent-framework-core[all]`을 지정하여 모든 통합 패키지를 한 번에 설치
- 탐색·개발 환경에 적합. 경량 환경에서는 필요한 패키지만 선택 설치 권장

```bash
# 설치 (모든 통합 패키지 자동 포함)
pip install agent-framework==1.0.0

# 선택적 설치 예시 (경량 환경)
pip install agent-framework-core          # 기본 (OpenAI/Azure OpenAI 포함)
pip install agent-framework-foundry       # Azure AI Foundry 추가
pip install agent-framework-copilotstudio --pre  # Copilot Studio (preview)

# 완전 제거 (하위 패키지 명시 필요)
pip uninstall -y agent-framework agent-framework-core agent-framework-openai agent-framework-foundry
```

---

### 2️⃣ `agent-framework-core` — 핵심 엔진

- 에이전트와 워크플로우의 **플랫폼 독립적인 핵심 추상화** 를 제공
- `[all]` extras를 통해 모든 통합 패키지를 선택적으로 포함할 수 있는 구조로 개편
- 직접 의존성: `pydantic`, `python-dotenv`, `opentelemetry-api`, `typing-extensions`
- 주요 제공 요소:
  - `Agent` — 에이전트 기본 클래스
  - `WorkflowBuilder` — 워크플로우 빌더
  - `WorkflowContext` — 실행 컨텍스트
  - `Executor`, `@handler`, `@executor` — 실행기 정의
  - 이벤트 시스템 (`WorkflowOutputEvent` 등)
  - MCP(Model Context Protocol) 지원 (`[all]` extras에 포함)

---

### 3️⃣ `agent-framework-openai` — OpenAI / Azure OpenAI 클라이언트 *(신규 GA)*

- 구버전의 `agent-framework-azure-ai`에서 **OpenAI/Azure OpenAI 관련 기능을 분리**한 패키지
- OpenAI API와 Azure OpenAI API 모두 지원
- 주요 제공 요소:
  - `OpenAIChatClient` — OpenAI Responses API 기반 채팅 클라이언트 **(신규 권장)**
  - `OpenAIChatCompletionClient` — Chat Completions API 기반 클라이언트 (하위 호환용)
  - `OpenAIEmbeddingClient` — 임베딩 클라이언트
- 의존성: `agent-framework-core`, `openai>=1.99.0`

---

### 4️⃣ `agent-framework-foundry` — Azure AI Foundry 통합 *(신규 GA)*

- 구버전의 `agent-framework-azure-ai`에서 **Azure AI Foundry 관련 기능을 분리**한 패키지
- Azure AI Foundry 프로젝트 연결 및 Foundry 전용 기능 담당
- 주요 제공 요소:
  - Foundry 채팅 클라이언트 및 사전 구성된 Foundry 에이전트
  - Foundry 임베딩 클라이언트
  - Foundry 메모리 프로바이더
- 의존성: `agent-framework-core`, `agent-framework-openai`, `azure-ai-inference`, `azure-ai-projects>=2.0.0`

---

### 5️⃣ `azure-ai-projects` — Azure Foundry SDK

- **Microsoft 공식 Azure SDK** 패키지 (2.x로 메이저 업그레이드됨)
- Azure AI Foundry 프로젝트에 대한 저수준 접근 제공
- 주요 역할:
  - Azure AI Foundry 프로젝트 엔드포인트 연결
  - 모델 배포 정보 조회
  - `DefaultAzureCredential` 기반 인증 처리
  - `agent-framework-foundry`가 내부적으로 의존

---

### 6️⃣ `agent-framework-orchestrations` — 오케스트레이션 패턴 *(beta)*

- 멀티 에이전트 워크플로우를 위한 **고수준 오케스트레이션 빌더** 제공
- 주요 제공 요소:
  - `SequentialBuilder` — 에이전트를 순차적으로 실행
  - `ConcurrentBuilder` — 에이전트를 병렬로 실행 후 결과 집계
  - `HandoffBuilder` — 에이전트 간 분산 라우팅
  - `GroupChatBuilder` — 오케스트레이터 주도 멀티 에이전트 대화
  - `MagenticBuilder` — Magentic One 패턴 기반 정교한 멀티 에이전트 오케스트레이션

---
