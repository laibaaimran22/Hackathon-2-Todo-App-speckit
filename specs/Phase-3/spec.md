# Phase 3: AI-Powered Todo Chatbot Specification

## Overview
Add a conversational AI chatbot to the existing Phase 2 todo application that allows users to manage tasks through natural language using Cohere AI and MCP (Model Context Protocol) for tool calling.

## Target Audience
Developers adding conversational AI to existing Phase 2 todo app

## Success Criteria
- Chatbot icon visible on dashboard
- Users can manage tasks through natural language
- Bot understands: add, view, update, delete, mark complete tasks
- Cohere agent calls backend APIs via MCP
- All Phase 2 features remain working
- Real-time UI updates after bot actions
- <3 second response time
- User authentication and isolation maintained

## Constraints
- Technology: Cohere AI (API key: JMfQBzVJJIdWvoFhgxTtft8uBYqclvrsRqgtmwzh)
- Framework: MCP (Model Context Protocol) for tool calling
- Build on: Phase 2 app (Next.js + FastAPI + Neon)
- Working directory: Phase-3/ folder
- Deployment: Vercel (frontend), Hugging Face (backend)
- Keep Phase 2 functionality intact

## Technical Stack
- Frontend: Next.js 15, TypeScript, Tailwind CSS
- Backend: FastAPI, Python
- AI: Cohere API
- Protocol: MCP (Model Context Protocol)
- Database: Neon PostgreSQL (existing)
- Auth: Better Auth JWT (existing)

## Dependencies to Add
- Frontend: cohere-ai, @modelcontextprotocol/sdk
- Backend: cohere, mcp

## Key Features to Build

### 1. Chat UI Components
- Floating chatbot icon (bottom-right of dashboard)
- Chat window (opens on click)
- Message display (user + bot messages)
- Input field (user types here)
- Minimize/close buttons
- Mobile responsive

### 2. Cohere Integration
- Setup Cohere client with API key
- Configure agent as "helpful todo assistant"
- Enable function calling capabilities
- Handle natural language understanding
- Maintain conversation context

### 3. MCP Tool Exposure
- Create MCP server in backend
- Expose 5 tools:
  * add_task - create new task
  * get_tasks - retrieve user's tasks
  * update_task - modify existing task
  * delete_task - remove task
  * mark_complete - toggle task status
- Include JWT authentication
- Enforce user isolation

### 4. Natural Language Handling
- Understand intent variations
- Extract task details from messages
- Handle contextual references
- Provide friendly responses

### 5. UI Integration
- Add chatbot to existing dashboard
- Real-time task list updates
- Show bot actions in UI immediately
- Error handling and feedback

## Example User Interactions
- "Add task to buy groceries" → Bot creates task, confirms: "Added 'Buy groceries' ✓"
- "Show my incomplete tasks" → Bot lists all pending tasks
- "Mark the first one as done" → Bot marks task complete, UI updates
- "Delete all completed tasks" → Bot removes completed tasks, confirms

## Architecture Flow
User → Chat UI → Cohere Agent → MCP Tools → FastAPI Backend → Neon DB

## Not Building
- Voice interface
- Multi-language support
- Advanced analytics
- Proactive notifications
- Calendar integration
- Offline mode

## Functional Requirements

### FR-001: Chat UI Component
- System shall display a floating chatbot icon on the dashboard
- System shall open a chat window when the icon is clicked
- System shall display user and bot messages in a conversation format
- System shall provide an input field for user messages
- System shall include minimize/close functionality

### FR-002: Cohere AI Integration
- System shall initialize Cohere client with provided API key
- System shall configure the AI agent as a helpful todo assistant
- System shall enable function calling for task management operations
- System shall maintain conversation context across interactions

### FR-003: MCP Tool Exposure
- System shall create an MCP server in the backend
- System shall expose 5 specific tools for task operations
- System shall authenticate requests using JWT tokens
- System shall enforce user isolation to prevent cross-user data access

### FR-004: Natural Language Processing
- System shall understand various phrasings for task operations
- System shall extract task details (title, description, etc.) from natural language
- System shall handle contextual references (e.g., "the first one", "that task")
- System shall provide helpful and friendly responses

### FR-005: UI Integration
- System shall update the task list in real-time after bot actions
- System shall maintain all existing Phase 2 functionality
- System shall provide appropriate error handling and feedback
- System shall be responsive on mobile devices

## Non-Functional Requirements

### NFR-001: Performance
- Response time shall be less than 3 seconds for typical queries
- System shall handle concurrent users efficiently

### NFR-002: Security
- Authentication shall be maintained using existing JWT tokens
- User data shall remain isolated between users
- API keys shall be stored securely in environment variables

### NFR-003: Usability
- Chat interface shall be intuitive and easy to use
- System shall provide helpful error messages
- System shall maintain consistent UI with existing application

## Acceptance Criteria

### AC-001: Chatbot Functionality
Given a user on the dashboard
When they interact with the chatbot
Then they can perform all basic task operations using natural language

### AC-002: Data Integrity
Given a user performs operations through the chatbot
When operations are completed
Then the task list updates in real-time and data remains consistent

### AC-003: User Isolation
Given multiple users using the chatbot simultaneously
When they perform operations
Then each user only sees and modifies their own tasks

### AC-004: Performance
Given a user sends a request to the chatbot
When the request is processed
Then the response is delivered within 3 seconds

## Error Handling
- Network errors during API calls shall be gracefully handled
- Invalid user inputs shall result in helpful error messages
- Authentication failures shall redirect to login or show appropriate error
- MCP communication failures shall be caught and reported to user