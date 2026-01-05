# Phase 2 Frontend: Architecture

## Directory Structure (Next.js 15 App Router)
```text
src/
├── app/                  # App Router
│   ├── (auth)/           # Auth group (login, register)
│   ├── (dashboard)/      # Protected dashboard routes
│   ├── api/              # Route handlers (Better Auth integration)
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Landing page
├── components/           # UI Components
│   ├── auth/             # Login/Signup forms
│   ├── dashboard/        # Task cards, lists, filters
│   ├── shared/           # Navbar, Footer, Buttons, Inputs
│   └── ui/               # Lower-level primitive components (Radix based)
├── hooks/                # Custom React hooks
├── lib/                  # Utilities (auth.ts - Better Auth config, utils.ts)
├── services/             # API interaction layer / Server Actions
├── types/                # TypeScript interfaces
└── middleware.ts         # Authentication protection & redirect logic
```

## Authentication Flow (Better Auth + JWT)
1. **Frontend**: Client-side form submits to Better Auth `signIn` or `signUp`.
2. **Better Auth Plugin**: Issues a JWT stored in secure `HttpOnly` cookies.
3. **Middleware**: Validates the session before granting access to `/(dashboard)` routes.
4. **Backend Integration**: FastAPI backend validates the JWT using a shared secret to extract `user_id`.

## Data Fetching Strategy
- **Server Components**: Used for initial list rendering in the Dashboard to minimize client-side bundle size.
- **Server Actions**: Used for mutations (Create, Update, Delete, Toggle).
- **Optimistic UI**: Implementation of `useOptimistic` for instantaneous feedback on task completion and deletion.

## Security
- **Secure Cookies**: HTTP-only, Secure, and SameSite=Lax.
- **Route Protection**: Middleware-level session checks.
- **CSP**: Implemented via Next.js headers.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
