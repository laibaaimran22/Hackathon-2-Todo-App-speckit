---
id: "001"
title: "Phase 3 Specification"
stage: "spec"
date: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "Phase-3"
branch: "main"
user: "laiba"
command: "/sp.specify"
labels: ["specification", "ai-chatbot", "todo-app", "mcp", "cohere"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "specs/Phase-3/spec.md"
  - "specs/Phase-3/plan.md"
  - "specs/Phase-3/tasks.md"
tests: []
---

# Phase 3: AI-Powered Todo Chatbot

Target audience: Developers adding conversational AI to existing Phase 2 todo app

IMPORTANT NOTES:
- Work in Phase-3/ folder (copied from Phase-2/)
- Specifications will be created in specs/Phase-3/
- Prompt history will be recorded in history/
- Phase 3 agents already exist in .claude/agents/
- Phase 3 skills already exist in .claude/skills/

Focus: Add chatbot UI and Cohere AI integration to existing todo application for natural language task management

Success criteria:
- Chatbot icon visible on dashboard
- Users can manage tasks through natural language
- Bot understands: add, view, update, delete, mark complete tasks
- Cohere agent calls backend APIs via MCP
- All Phase 2 features remain working
- Real-time UI updates after bot actions
- <3 second response time
- User authentication and isolation maintained

Constraints:
- Technology: Cohere AI (API key: JMfQBzVJJIdWvoFhgxTtft8uBYqclvrsRqgtmwzh)
- Framework: MCP (Model Context Protocol) for tool calling
- Build on: Phase 2 app (Next.js + FastAPI + Neon)
- Working directory: Phase-3/ folder
- Deployment: Vercel (frontend), Hugging Face (backend)
- Keep Phase 2 functionality intact

Key Features to Build:

1. Chat UI Components
   - Floating chatbot icon (bottom-right of dashboard)
   - Chat window (opens on click)
   - Message display (user + bot messages)
   - Input field (user types here)
   - Minimize/close buttons
   - Mobile responsive

2. Cohere Integration
   - Setup Cohere client with API key
   - Configure agent as "helpful todo assistant"
   - Enable function calling capabilities
   - Handle natural language understanding
   - Maintain conversation context

3. MCP Tool Exposure
   - Create MCP server in backend
   - Expose 5 tools:
     * add_task - create new task
     * get_tasks - retrieve user's tasks
     * update_task - modify existing task
     * delete_task - remove task
     * mark_complete - toggle task status
   - Include JWT authentication
   - Enforce user isolation

4. Natural Language Handling
   - Understand intent variations
   - Extract task details from messages
   - Handle contextual references
   - Provide friendly responses

5. UI Integration
   - Add chatbot to existing dashboard
   - Real-time task list updates
   - Show bot actions in UI immediately
   - Error handling and feedback

Example User Interactions:

"Add task to buy groceries"
→ Bot creates task, confirms: "Added 'Buy groceries' ✓"

"Show my incomplete tasks"
→ Bot lists all pending tasks

"Mark the first one as done"
→ Bot marks task complete, UI updates

"Delete all completed tasks"
→ Bot removes completed tasks, confirms

Technical Stack:
- Frontend: Next.js 15, TypeScript, Tailwind CSS
- Backend: FastAPI, Python
- AI: Cohere API
- Protocol: MCP (Model Context Protocol)
- Database: Neon PostgreSQL (existing)
- Auth: Better Auth JWT (existing)