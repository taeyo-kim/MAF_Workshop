<div align="center">

# 🚀 MAF Workshop

### Microsoft Agent Framework  실습 가이드

[![Framework](https://img.shields.io/badge/Framework-MAF-blue?style=for-the-badge)](https://learn.microsoft.com/en-us/agent-framework/tutorials/overview)
[![Status](https://img.shields.io/badge/Status-GA-blue?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()

</div>

---
### **업데이트 정보**  

**<span style="color: #3708e0;">마지막 업데이트 날짜 : 2026.04.03</span>**

**📢 4월 3일 정식버전이 GA 되었지만, GA 버전에서도 RC 대비 일부 Breaking Change가 발생한 것으로 보이기에, 하기 실습을 전면 재검토 중입니다. 현재 **19번** 까지는 올바로 동작하는 것을 확인했습니다.  
19번 이후 실습은 현재 검토 및 수정 중에 있으며, 최대한 빠르게 업데이트할 예정입니다.** 

---

현재 리포를 Fork하거나 Clone하여 로컬에서 Visual Studio Code로 실습을 진행하실 수 있습니다.
```bash
git clone https://github.com/taeyo-kim/MAF_Workshop.git  
cd MAF_Workshop
code .
```

## 📖 개요

> **Microsoft Agent Framework (MAF) 실습 워크샵에 오신 것을 환영합니다!**

이 워크샵은 [Microsoft Learn의 공식 MAF 문서](https://learn.microsoft.com/en-us/agent-framework/tutorials/overview)를 기반으로 재구성되었습니다.

> **⚠️ 중요 알림**  
> 정식버전 출시 : **2026년 4월 3일** 1.0.0 버전이 정식 출시되었습니다!
> 정식 출시 후에는 [공식 문서](https://learn.microsoft.com/en-us/agent-framework/tutorials/overview)를 기준으로 실습을 진행하시길 권장합니다. 물론, 이 워크샵도 계속해서 유용한 참고 자료가 될 것입니다! (제가 업데이트를 한다면 말이죠 😉)

---

## 🎯 MAF 학습 경로

### 필수 사전 준비사항

- ⚙️ [**Prerequisite**](MAF/0.Prerequisite.ipynb) - 사전 준비 및 환경 설정

### 📘 기본 이해

- 🌟 1. [**Overview**](MAF/Overview.ipynb) - MAF 개요 및 아키텍처  
- 📱 2. [**Agent 유형들**](MAF/Agent-Type.ipynb) - 에이전트 유형 및 기능 비교    
    (옵션) [**MAF 라이브러리**](MAF/MAF-packages.md) - MAF 패키지 구조 및 역할 설명

### 📗 실습

- 🤖 3. [**Agent 생성**](MAF/1.CreateAgent.ipynb) - 에이전트 생성 기본
- 💬 4. [**Multi-turn Agent**](MAF/2.Multi-turn-Conversation.ipynb) - 다중턴 대화 구현
- 🛠️ 5. [**Function Tool**](MAF/3.Function-Tool.ipynb) - Function 도구 사용법
- 👤 6. [**Human In Loop 패턴**](MAF/4.Human-In-Loop.ipynb) - 휴먼 개입 패턴 구현
- 📊 7. [**Structured Output**](MAF/5.Structured-Output.ipynb) - 구조화된 출력 생성
- 🔧 8. [**Agent as Function**](MAF/6.Agent-as-function-tool.ipynb) - 에이전트를 Function 도구로 활용
- 🔌 9. [**Agent with MCP Tool**](MAF/7.Agent-as-MCP-tool.ipynb) - 에이전트를 MCP 도구로 활용(사용 및 제공)
- 🔩 10. [**Agent with Middleware**](MAF/9.Agent-with-Middleware.ipynb) - 미들웨어 추가 및 활용
- 📈 11. [**Observability**](MAF/8.Observability.ipynb) - 에이전트 관찰성(Observability) 구현
- 💿 12. [**Persist and Resume**](MAF/10.Persist-and-Resume.ipynb) - 에이전트 상태 저장 및 복원
---

### ☁️ Microsoft Foundry Agent 통합

- 📢 13. [**FoundryAgent 생성 및 활용**](MAF/AzureAIFoundryAgent.ipynb) - Microsoft Foundry 기반 에이전트 생성 및 활용
- 📱 14. [**배포된 Agent 활용**](MAF/Using-Published-Agent.ipynb) - 배포된 Foundry Agent 활용하기  
- 🤖 15. [**FoundryAgent와 MCP**](MAF/Foundry_Agent_MCP.ipynb) - Foundry Agent에서 Hosted MCP 도구 활용하기 
- 🚀 16. [**Hosted Agent 배포**](HostedAgent-Lab/Deploy-HostedAgent.ipynb) - Hosted Agent 배포하기 (선택, Option)

---

### 🔄 워크플로우 실습

- 🔗 17. [**Workflow Overview**](MAF/20.workflow.ipynb) - MAF 워크플로우 개념 및 구현
- 🔀 18. [**Simple Sequential Workflow**](MAF/21.SimpleSequentialWorkflow.ipynb) - 간단한 순차 워크플로우 구현
- 🎭 19. [**Agents in Workflow**](MAF/22.Agents-In-Workflow.ipynb) - 워크플로우에서 에이전트 사용하기

---

### 🖥️ 개발 도구 연계 (필수)

🎨 **DevUI 사용**

- 🔮 20. [**DevUI**](MAF/DevUI/intro.ipynb) - DevUI: 에이전트 및 워크플로우 테스트 앱

🧸 **AG-UI를 활용한 서버/클라이언트 구축**

- 🧿 21. [**AG-UI: Build Server**](AG-UI/01.Build-server.ipynb) - AG-UI를 활용한 에이전트 서버 생성 및 테스트
- 🧿 22. [**AG-UI: CopilotKit**](AG-UI/03.CopilotKit.ipynb) - CopilotKit을 활용하여 빠르게 UI 제공하기
- 🧿 [**AG-UI: Build Client**](AG-UI/02.Build-client.ipynb) - AG-UI를 활용한 에이전트 클라이언트 만들기

---

### 📂 AI-SEARCH + MAF 실습

- 🔍 [**AI-SEARCH/Agent-Search**](AI-SEARCH/Agent-Search.ipynb) - MAF Agent와 Azure AI Search 연동 예제
    : 이 실습은 [Azure AI Search with Document Intelligence](https://github.com/hijigoo/azure-ai-search-with-doc-intelligence) 워크샵을 기반으로 하여 Azure AI Search를 구성하고, 그 이후 MAF Agent의 통합하는 샘플 코드를 제공합니다.

---

### 🧿 기타 정보

- FAQ  : https://learn.microsoft.com/en-us/azure/ai-foundry/agents/faq?view=foundry  
- Quotas, limits, models, and regional support : https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/limits-quotas-regions?view=foundry
