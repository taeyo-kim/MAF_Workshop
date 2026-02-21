"use client";

import { CopilotSidebar } from "@copilotkit/react-ui";

export default function Page() {
  return (
    <main>
      <CopilotSidebar
        labels={{
          title: "Your Assistant",
          initial: "Hi! How can I help you today?",
        }}
      />
      <span className="badge">AI Powered</span>
      <h1>Your App</h1>
      <p>사이드바를 열어 AI 어시스턴트와 대화를 시작해 보세요.</p>
    </main>
  );
}