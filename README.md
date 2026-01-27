# MAF Workshop (updated 01.27.2026)

## 🤖 Microsoft Agent Framework (MAF) 가벼운 실습

이 실습은 Microsoft Learn 사이트의 [**MAF 공식 문서**](https://learn.microsoft.com/en-us/agent-framework/tutorials/overview)를 기반으로 재구성하였습니다. MAF V2는 아직 Preview 상태이기에 간혹 공식 문서의 코드가 올바로 동작하지 않는 문제가 있어서 이를 개선하고자 별도의 가벼운 실습 워크샵을 여기에 작성하고 있는 것입니다. 공식 사이트의 문서는 아래 링크에서 확인할 수 있으며, 계속해서 개선되고 업데이트 될 것이기에 최신 정보를 확인하시려면 공식 문서를 참고하시기 바랍니다. V2가 공식 출시되면 그 시점에는 공식 사이트를 기준으로 실습을 진행하는 것을 권장드립니다.

https://learn.microsoft.com/en-us/agent-framework/tutorials/overview

## 🪄 Agent 실습

#### 기본 설정 및 시작하기
- [**0.Prerequisite.ipynb**](MAF/0.Prerequisite.ipynb) - 사전 준비 사항 및 환경 설정
- [**1.CreateAgnet.ipynb**](MAF/1.CreateAgnet.ipynb) - 에이전트 생성 기초

#### 에이전트 기본 기능
- [**2.Multi-turn-Conversation.ipynb**](MAF/2.Multi-turn-Conversation.ipynb) - 다중 턴 대화 구현
- [**3.Function-Tool.ipynb**](MAF/3.Function-Tool.ipynb) - Function 도구 사용법
- [**4.Human-In-Loop.ipynb**](MAF/4.Human-In-Loop.ipynb) - 휴먼 개입 패턴 구현
- [**5.Structured-Output.ipynb**](MAF/5.Structured-Output.ipynb) - 구조화된 출력 생성 (현재 작업 중)

#### 에이전트 고급 기능
- [**6.Agent-as-function-tool.ipynb**](MAF/6.Agent-as-function-tool.ipynb) - 에이전트를 Function 도구로 활용
- [**7.Agent-as-MCP-tool.ipynb**](MAF/7.Agent-as-MCP-tool.ipynb) - 에이전트를 MCP 도구로 활용

#### 관찰성 및 미들웨어
- [**8.Observability.ipynb**](MAF/8.Observability.ipynb) - 에이전트 관찰성(Observability) 구현
- [**9.Agent-wirh-Middleware.ipynb**](MAF/9.Agent-wirh-Middleware.ipynb) - 미들웨어 추가 및 활용

#### 상태 관리 및 메모리
- [**10.Persist-and-Resume.ipynb**](MAF/10.Persist-and-Resume.ipynb) - 에이전트 상태 저장 및 복원
- [**11.ExternalStroage-Redis.ipynb**](MAF/11.ExternalStroage-Redis.ipynb) - Redis를 활용한 외부 스토리지 연동
- [**12.Memory_Agent.ipynb**](MAF/12.Memory_Agent.ipynb) - 메모리 기능을 가진 에이전트 구현(현재 작업 중)

---

## 🔄 Workflow 실습
- [**21.SimpleSequentialWorkflow.ipynb**](21.SimpleSequentialWorkflow.ipynb) - 간단한 순차 워크플로우 구현
- [**22.Agents-In-Workflow.ipynb**](22.Agents-In-Workflow.ipynb) - 워크플로우에서 에이전트 사용하기

---
