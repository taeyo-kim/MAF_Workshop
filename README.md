<div align="center">

# 🚀 MAF Workshop

### Microsoft Agent Framework  실습 가이드

*Last Updated: 2026.02.24*

[![Framework](https://img.shields.io/badge/Framework-MAF-blue?style=for-the-badge)](https://learn.microsoft.com/en-us/agent-framework/tutorials/overview)
[![Status](https://img.shields.io/badge/Status-RC-yellow?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()

</div>

---

## 📖 개요

> **Microsoft Agent Framework (MAF) 실습 워크샵에 오신 것을 환영합니다!**

이 워크샵은 [Microsoft Learn의 공식 MAF 문서](https://learn.microsoft.com/en-us/agent-framework/tutorials/overview)를 기반으로 재구성되었습니다.

### 💡 왜 이 워크샵이 필요한가요?

MAF는 현재 **RC 단계**로, 공식 문서의 일부 코드가 올바르게 동작하지 않는 경우가 있습니다. 이 워크샵은 이러한 문제를 해결하고 실무에서 바로 적용 가능한 실습 환경을 제공합니다.

> **⚠️ 중요 알림**  
> 정식버전 출시 예정 : **2026년 2월 말 ~ 3월 초 추정** (일정 변경 가능)  
> 정식 출시 후에는 [공식 문서](https://learn.microsoft.com/en-us/agent-framework/tutorials/overview)를 기준으로 실습을 진행하시길 권장합니다. 물론, 이 워크샵도 계속해서 유용한 참고 자료가 될 것입니다! (제가 업데이트를 한다면 말이죠 😉)

---

## 🎯 학습 경로

### 필수 사전 준비사항

- ⚙️ [**Prerequisite**](MAF/0.Prerequisite.ipynb) - 사전 준비 및 환경 설정

### 📘 기본 이해

- 🌟 1. [**Overview**](MAF/Overview.ipynb) - MAF 개요 및 아키텍처
- 📱 2. [**Agent-Type**](MAF/Agent-Type.ipynb) - 에이전트 유형 및 기능 비교

### 📗 실습

- 🤖 3. [**Create-Agent**](MAF/1.CreateAgent.ipynb) - 에이전트 생성 기본
- 💬 4. [**Multi-turn**](MAF/2.Multi-turn-Conversation.ipynb) - 다중턴 대화 구현
- 🛠️ 5. [**Function-Tool**](MAF/3.Function-Tool.ipynb) - Function 도구 사용법
- 👤 6. [**Human-In-Loop**](MAF/4.Human-In-Loop.ipynb) - 휴먼 개입 패턴 구현
- 📊 7. [**Structured-Output**](MAF/5.Structured-Output.ipynb) - 구조화된 출력 생성
- 🔌 8. [**Agent-as-Function**](MAF/6.Agent-as-function-tool.ipynb) - 에이전트를 Function 도구로 활용
- 🔌 9. [**Agent-with-Middleware**](MAF/9.Agent-with-Middleware.ipynb) - 미들웨어 추가 및 활용
- 📈 10. [**Observability**](MAF/8.Observability.ipynb) - 에이전트 관찰성(Observability) 구현


#### 💾 상태 관리 (공사중)

- 💿 [**10.Persist-and-Resume**](MAF/10.Persist-and-Resume.ipynb) - 에이전트 상태 저장 및 복원
- 🗄️ [**11.ExternalStorage-Redis**](MAF/11.ExternalStroage-Redis.ipynb) - Redis를 활용한 외부 스토리지 연동
- 🧠 [**12.Memory_Agent**](MAF/12.Memory_Agent.ipynb) - 메모리 기능을 가진 에이전트 구현

---

## ☁️ Microsoft Foundry 통합

### 🌟 Azure AI Foundry 연동 (**중요 🔔**)

- 📢 [**AzureAIFoundryAgent**](MAF/AzureAIFoundryAgent.ipynb) - Microsoft Foundry 기반 에이전트 생성 및 활용 (**Classic과 New Portal 모두 포함**)
- 📢 [**Using-Published-Agent**](MAF/Using-Published-Agent.ipynb) - 배포 및 게시된 Foundry Agent 활용하기 (⚠️**PREVIEW**)
- 🚀 [**Deploy-HostedAgent**](HostedAgent-Lab/Deploy-HostedAgent.ipynb) - Hosted Agent 배포하기

---

## 🔄 워크플로우 실습

### 연결 및 조율

- 🔗 [**20.Workflow_Overview**](MAF/20.workflow.ipynb) - MAF 워크플로우 개념 및 구현
- 🔀 [**21.SimpleSequentialWorkflow**](MAF/21.SimpleSequentialWorkflow.ipynb) - 간단한 순차 워크플로우 구현
- 🎭 [**22.Agents-In-Workflow**](MAF/22.Agents-In-Workflow.ipynb) - 워크플로우에서 에이전트 사용하기

---

## ⚡ 특별 워크샵

### ✈️ 1시간 핵심 워크샵: 여행 계획 에이전트

> **빠른 시작 가이드**  By [wedding-crasher](https://github.com/wedding-crasher)

📚 [**Travel-Planner-Workshop**](https://github.com/wedding-crasher/MAF_Workshop/tree/main/SUPER-FAST-WORKSHOP) - 1시간 만에 여행 계획 에이전트 만들기  
    - 이 워크샵은 wedding-crasher님의 Repo에서 계속해서 업데이트가 되고 있습니다. 그렇기에, 링크를 해당 Repo로 변경했습니다.

---

## 🖥️ 개발 도구

### 🎨 DevUI 사용

- 🔮 [**DevUI/intro**](MAF/DevUI/intro.ipynb) - DevUI: 에이전트 및 워크플로우 테스트 앱

### 🧸 AG-UI를 활용한 서버/클라이언트 구축

- 🧿 [**AG-UI/01.Build-server**](AG-UI/01.Build-server.ipynb) - AG-UI를 활용한 에이전트 서버 생성 및 테스트
- 🧿 [**AG-UI/03.CopilotKit**](AG-UI/03.CopilotKit.ipynb) - CopilotKit을 활용하여 빠르게 UI 제공하기
- 🧿 [**AG-UI/02.Build-client**](AG-UI/02.Build-client.ipynb) - AG-UI를 활용한 에이전트 클라이언트 만들기

---

## 📂 AI-SEARCH + MAF 실습

- 🔍 [**AI-SEARCH/Agent-Search**](AI-SEARCH/Agent-Search.ipynb) - MAF Agent와 Azure AI Search 연동 예제
    : 이 실습은 [Azure AI Search with Document Intelligence](https://github.com/hijigoo/azure-ai-search-with-doc-intelligence) 워크샵을 기반으로 하여 Azure AI Search를 구성하고, 그 이후 MAF Agent의 통합하는 샘플 코드를 제공합니다.

---

## 🧿 기타 정보

- FAQ  : https://learn.microsoft.com/en-us/azure/ai-foundry/agents/faq?view=foundry  
- Quotas, limits, models, and regional support : https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/limits-quotas-regions?view=foundry
