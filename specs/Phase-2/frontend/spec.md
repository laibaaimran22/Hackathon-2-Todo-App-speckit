# Phase 2 Frontend: Specification

## 1. Executive Summary
The Phase 2 Frontend is a modern, responsive web application built with Next.js 15. It replaces the Phase 1 CLI with a full-stack interface, featuring secure authentication via Better Auth and comprehensive task management (CRUD) integrated with a FastAPI backend.

## 2. Technical Stack
- **Framework**: Next.js 15 (App Router)
- **Authentication**: Better Auth (JWT Plugin)
- **Styling**: Tailwind CSS
- **Interactions**: Server Actions & React 19 Hooks (`useOptimistic`, `useActionState`)
- **Validation**: Zod + React Hook Form

## 3. Core Requirements
- **Authentication**: Email/Password flow, Persistent sessions.
- **CRUD Operations**: Create, Read (List), Update (Edit/Toggle), Delete.
- **User Privacy**: Strict data isolation via JWT `sub` claim.
- **Performance**: Mobile-first, <1s FCP, Optimistic UI for mutations.

## 4. Security
- **JWT Isolation**: Frontend sends session cookies; backend validates and extracts `user_id`.
- **HttpOnly Cookies**: All session data is inaccessible to client-side scripts.
- **Route Guard**: Middleware ensures `/(dashboard)` routes require an active session.

## 5. Deployment
- **Hosting**: Optimized for Vercel.
- **Config**: Environment variables for `API_URL` and `JWT_SECRET`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
