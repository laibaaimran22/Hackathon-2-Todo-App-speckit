# Phase 2 Frontend: API Contract

This document defines the interface between the Next.js Frontend and the FastAPI Backend, primarily navigated via Server Actions for Phase 2.

## 1. Authentication (Better Auth)
The application uses **Better Auth** with the **JWT Plugin**.

### Auth Endpoints (Client SDK)
- `signIn.email()`: POST request to `/api/auth/sign-in`
- `signUp.email()`: POST request to `/api/auth/sign-up`
- `signOut()`: POST request to `/api/auth/sign-out`
- `getSession()`: GET request to `/api/auth/get-session`

## 2. Todo Operations (Server Actions)
Server Actions provide the interface for data mutations, ensuring type safety and reduced client-side shipping.

### `getTasks()`
- **Output**: `Task[]`
- **Scope**: Filtered by authenticated `user_id`.

### `createTask(data)`
- **Input**: `{ title: string, content?: string, priority: 'low' | 'medium' | 'high' }`
- **Output**: Created `Task` object.

### `updateTask(id, data)`
- **Input**: `id: string`, `data: Partial<Task>`
- **Output**: Updated `Task` object.

### `deleteTask(id)`
- **Input**: `id: string`
- **Output**: `{ success: boolean }`

### `toggleTaskStatus(id)`
- **Input**: `id: string`
- **Output**: `{ success: boolean, status: string }`

## 3. Data Models (TypeScript)
```typescript
interface Task {
  id: string;
  userId: string;
  title: string;
  content?: string;
  is_completed: boolean;
  priority: 'low' | 'medium' | 'high';
  createdAt: Date;
  updatedAt: Date;
}

interface User {
  id: string;
  email: string;
  name: string;
}
```

## 4. Error Schema
```json
{
  "error": {
    "code": "VALIDATION_ERROR | AUTH_ERROR | SERVER_ERROR",
    "message": "Human readable message",
    "fields": { "field_name": "Error description" }
  }
}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
