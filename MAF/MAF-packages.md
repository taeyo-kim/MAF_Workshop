# 📦 MAF 핵심 라이브러리 역할

Microsoft Agent Framework(MAF)는 여러 패키지로 구성된 계층적 의존성 구조를 가집니다.

---

## 📋 라이브러리 역할 요약

| 라이브러리 | 계층 | 역할 |
|-----------|------|------|
| `agent-framework` | 최상위 메타 패키지 | 모든 하위 패키지를 한 번에 설치하는 **umbrella 패키지**. 실제 코드는 없고, 의존성 묶음 역할 |
| `agent-framework-core` | 핵심 엔진 | 에이전트·워크플로우·실행기(Executor)·이벤트·WorkflowBuilder 등 **플랫폼 독립적인 핵심 추상화** 를 제공. Azure 없이도 사용 가능 |
| `agent-framework-azure-ai` | Azure 통합 어댑터 | `AzureOpenAIChatClient`, Azure AI Foundry 연결 등 **Azure 전용 구현체** 를 제공. `agent-framework-core`의 인터페이스를 Azure 서비스로 연결 |
| `azure-ai-projects` | Azure SDK | Azure AI Foundry 프로젝트에 접근하는 **Microsoft 공식 Azure SDK**. 엔드포인트 연결, 모델 배포 정보 조회, 인증 처리 등 담당 |

---

## 🗂️ 의존 관계 흐름

```
agent-framework  (설치 편의용 메타 패키지)
    ├── agent-framework-core       ← 핵심 추상화 (플랫폼 독립)
    └── agent-framework-azure-ai   ← Azure 구현체
            └── azure-ai-projects  ← Azure Foundry SDK (Microsoft 공식)
```

---

## 🔍 각 라이브러리 상세 설명

### 1️⃣ `agent-framework` — 메타 패키지

- 실제 코드를 포함하지 않는 **umbrella 패키지**
- `agent-framework-core`, `agent-framework-azure-ai` 등을 한 번에 설치
- **설치 시**: `pip install agent-framework --pre` 한 줄로 모든 의존성 설치 완료
- **제거 시**: 하위 패키지들을 명시적으로 나열해야 완전 제거 가능

```bash
# 설치 (하위 패키지 자동 포함)
pip install agent-framework==1.0.0b260130 --pre

# 완전 제거 (하위 패키지 명시 필요)
pip uninstall -y agent-framework agent-framework-core agent-framework-azure-ai azure-ai-projects
```

---

### 2️⃣ `agent-framework-core` — 핵심 엔진

- 에이전트와 워크플로우의 **플랫폼 독립적인 핵심 추상화** 를 제공
- Azure 없이도 단독으로 사용 가능
- 주요 제공 요소:
  - `Agent` — 에이전트 기본 클래스
  - `WorkflowBuilder` — 워크플로우 빌더
  - `WorkflowContext` — 실행 컨텍스트
  - `Executor`, `@handler`, `@executor` — 실행기 정의
  - 이벤트 시스템 (`WorkflowOutputEvent` 등)

---

### 3️⃣ `agent-framework-azure-ai` — Azure 통합 어댑터

- `agent-framework-core`의 인터페이스를 **Azure AI 서비스로 연결** 하는 구현체
- Azure OpenAI, Azure AI Foundry와의 통합 담당
- 주요 제공 요소:
  - `AzureOpenAIChatClient` — Azure OpenAI 연결 클라이언트
  - Azure AI Foundry 기반 에이전트 실행 지원

---

### 4️⃣ `azure-ai-projects` — Azure Foundry SDK

- **Microsoft 공식 Azure SDK** 패키지
- Azure AI Foundry 프로젝트에 대한 저수준 접근 제공
- 주요 역할:
  - Azure AI Foundry 프로젝트 엔드포인트 연결
  - 모델 배포 정보 조회
  - `DefaultAzureCredential` 기반 인증 처리
  - `agent-framework-azure-ai`가 내부적으로 의존

---
