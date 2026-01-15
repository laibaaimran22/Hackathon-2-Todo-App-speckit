# Phase 3: AI-Powered Todo Chatbot - Tasks

## Overview
Implementation tasks for adding an AI-powered chatbot to the Phase 2 todo application using Cohere AI and MCP.

## Sprint 1: Infrastructure Setup

### Task 1.1: MCP Server Setup
- **Description**: Set up MCP server in the backend to handle AI tool calls
- **Acceptance Criteria**:
  - MCP server runs alongside existing FastAPI backend
  - Server can register and expose tools to Cohere AI
  - Proper error handling for MCP communications
- **Tests**:
  - [x] MCP server starts without errors
  - [x] Tools are properly registered with MCP
  - [x] Error handling works for invalid requests
- **Files**: `Phase-3/backend/mcp_server.py`

### Task 1.2: Cohere Client Integration
- **Description**: Integrate Cohere AI client with proper API key configuration
- **Acceptance Criteria**:
  - Cohere client initialized with provided API key
  - Proper environment variable configuration
  - Function calling capabilities enabled
- **Tests**:
  - [x] Cohere client can be instantiated
  - [x] Environment variables are properly loaded
  - [x] Function calling is enabled and working
- **Files**: `Phase-3/frontend/lib/cohere-client.ts`

### Task 1.3: JWT Authentication for MCP
- **Description**: Implement JWT token validation for MCP tool calls
- **Acceptance Criteria**:
  - All MCP tool calls require valid JWT token
  - User isolation enforced based on token
  - Proper error responses for invalid tokens
- **Tests**:
  - [x] Valid tokens allow access to tools
  - [x] Invalid tokens return 401 errors
  - [x] Tokens restrict access to user's own data
- **Files**: `Phase-3/backend/mcp_auth.py`

## Sprint 2: Core Functionality

### Task 2.1: Implement add_task MCP Tool
- **Description**: Create MCP tool for adding new tasks via natural language
- **Acceptance Criteria**:
  - Tool accepts task details from AI
  - Creates task in database with proper user association
  - Returns success/error response to AI
- **Tests**:
  - [x] Tool can create tasks with title and description
  - [x] Task is associated with correct user
  - [x] Proper error handling for invalid inputs
- **Files**: `Phase-3/backend/tools/task_operations.py`

### Task 2.2: Implement get_tasks MCP Tool
- **Description**: Create MCP tool for retrieving user's tasks
- **Acceptance Criteria**:
  - Tool retrieves tasks filtered by user ID
  - Returns tasks in format suitable for AI consumption
  - Handles filtering options (all, completed, pending)
- **Tests**:
  - [x] Tool returns correct user's tasks
  - [x] Filtering options work properly
  - [x] Empty results handled gracefully
- **Files**: `Phase-3/backend/tools/task_operations.py`

### Task 2.3: Implement update_task MCP Tool
- **Description**: Create MCP tool for updating existing tasks
- **Acceptance Criteria**:
  - Tool can update task properties (title, description, etc.)
  - Validates user ownership of task
  - Returns updated task information
- **Tests**:
  - [x] Task updates work for valid requests
  - [x] Unauthorized updates are prevented
  - [x] Partial updates are supported
- **Files**: `Phase-3/backend/tools/task_operations.py`

### Task 2.4: Implement delete_task MCP Tool
- **Description**: Create MCP tool for deleting tasks
- **Acceptance Criteria**:
  - Tool deletes specified task with proper validation
  - Ensures user owns the task before deletion
  - Returns success confirmation
- **Tests**:
  - [x] Valid task deletions work correctly
  - [x] Unauthorized deletions are prevented
  - [x] Non-existent task deletions handled gracefully
- **Files**: `Phase-3/backend/tools/task_operations.py`

### Task 2.5: Implement mark_complete MCP Tool
- **Description**: Create MCP tool for toggling task completion status
- **Acceptance Criteria**:
  - Tool toggles completion status of specified task
  - Validates user ownership of task
  - Returns updated task status
- **Tests**:
  - [x] Task completion toggles work correctly
  - [x] Unauthorized toggles are prevented
  - [x] Task status updates properly in database
- **Files**: `Phase-3/backend/tools/task_operations.py`

## Sprint 3: UI Implementation

### Task 3.1: Create Chatbot UI Components
- **Description**: Develop floating chatbot UI with message display and input
- **Acceptance Criteria**:
  - Floating chatbot icon appears on dashboard
  - Clicking icon opens chat window
  - Messages display in conversation format
  - Input field allows user to type messages
- **Tests**:
  - [x] Chatbot icon appears correctly on dashboard
  - [x] Chat window opens/closes properly
  - [x] Messages display with proper styling
  - [x] Input field accepts text and submits
- **Files**: `Phase-3/frontend/src/components/chat/ChatBotIcon.tsx`, `Phase-3/frontend/src/components/chat/ChatWindow.tsx`

### Task 3.2: Implement Chat Message Display
- **Description**: Create components to display user and AI messages
- **Acceptance Criteria**:
  - Different styling for user vs AI messages
  - Loading indicators during AI processing
  - Error messages for failed requests
- **Tests**:
  - [x] User messages styled differently from AI messages
  - [x] Loading indicators appear during processing
  - [x] Error states are properly displayed
- **Files**: `Phase-3/frontend/src/components/chat/MessageBubble.tsx`

### Task 3.3: Connect Chat UI to MCP Backend
- **Description**: Implement communication between chat UI and MCP server
- **Acceptance Criteria**:
  - Messages sent from UI reach MCP server
  - AI responses are displayed in UI
  - Proper error handling for connection issues
- **Tests**:
  - [x] Messages are sent to MCP server
  - [x] Responses are received and displayed
  - [x] Connection errors are handled gracefully
- **Files**: `Phase-3/frontend/src/hooks/useChatBot.ts`

## Sprint 4: Integration and Real-time Updates

### Task 4.1: Real-time Task List Updates
- **Description**: Update task list in real-time when bot performs operations
- **Acceptance Criteria**:
  - Task list updates immediately after bot actions
  - No page refresh required for updates
  - Consistent state between bot and UI
- **Tests**:
  - [x] Task list updates after bot adds task
  - [x] Task list updates after bot marks task complete
  - [x] Task list updates after bot deletes task
- **Files**: `Phase-3/frontend/src/components/todo/ClientTodoDataSection.tsx`

### Task 4.2: Natural Language Intent Recognition
- **Description**: Improve AI's ability to recognize various ways to express intents
- **Acceptance Criteria**:
  - AI understands multiple ways to request task operations
  - Handles contextual references ("the first one", "that task")
  - Provides helpful responses for unrecognized commands
- **Tests**:
  - [x] Various phrasings for adding tasks work
  - [x] Contextual references are understood
  - [x] Unrecognized commands get helpful responses
- **Files**: `Phase-3/backend/ai_intents.py`

### Task 4.3: Chat History and Context Management
- **Description**: Maintain conversation context across multiple exchanges
- **Acceptance Criteria**:
  - AI remembers context from previous messages
  - Conversation history is maintained during session
  - Context is properly cleared when chat is closed
- **Tests**:
  - [x] AI responds appropriately to follow-up questions
  - [x] Context persists during conversation
  - [x] Context is cleared when chat closes
- **Files**: `Phase-3/frontend/src/context/ChatContext.tsx`

## Sprint 5: Testing and Polish

### Task 5.1: Comprehensive Testing
- **Description**: Test all chatbot functionality with various inputs
- **Acceptance Criteria**:
  - All task operations work through chat interface
  - Edge cases are handled properly
  - Error scenarios are gracefully managed
- **Tests**:
  - [x] Add task functionality works via chat
  - [x] View tasks functionality works via chat
  - [x] Update task functionality works via chat
  - [x] Delete task functionality works via chat
  - [x] Mark complete functionality works via chat
- **Files**: `Phase-3/tests/test_chatbot_integration.py`

### Task 5.2: Performance Optimization
- **Description**: Optimize response times and resource usage
- **Acceptance Criteria**:
  - AI responses delivered in <3 seconds
  - Minimal resource usage during idle periods
  - Efficient data fetching and updates
- **Tests**:
  - [x] Response times are consistently under 3 seconds
  - [x] Memory usage is reasonable
  - [x] Network requests are optimized
- **Files**: `Phase-3/frontend/src/lib/performance.ts`

### Task 5.3: Mobile Responsiveness
- **Description**: Ensure chatbot UI works well on mobile devices
- **Acceptance Criteria**:
  - Chat interface is usable on mobile screens
  - Touch targets are appropriately sized
  - Layout adapts to different screen sizes
- **Tests**:
  - [x] Chat window is usable on mobile
  - [x] Messages display properly on small screens
  - [x] Input field is accessible on mobile
- **Files**: `Phase-3/frontend/src/components/chat/ChatWindow.tsx`

### Task 5.4: Final Integration and Cleanup
- **Description**: Integrate chatbot into existing dashboard and clean up
- **Acceptance Criteria**:
  - Chatbot seamlessly integrates with existing UI
  - All Phase 2 functionality remains intact
  - Code follows existing project patterns and standards
- **Tests**:
  - [x] Chatbot appears on dashboard without breaking layout
  - [x] All existing functionality still works
  - [x] Code quality meets project standards
- **Files**: `Phase-3/frontend/src/app/dashboard/DashboardClient.tsx`