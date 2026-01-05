# Next.js Architecture Skill

## Overview
This skill specializes in architecting and implementing high-performance, scalable web applications using **Next.js 15 (App Router)**. It focuses on the separation of concerns, performance optimization, and developer experience.

## Capabilities
- **Routing & Layouts**: Expert implementation of the App Router, including nested layouts, parallel routes, and intercepted routes.
- **Server Components (RSC)**: Strategic use of Server Components for data fetching to minimize client-side JavaScript.
- **Client Components**: Precise implementation of interactive elements while maintaining server-side rendering benefits.
- **Server Actions**: Implementation of secure, type-safe data mutations and form handling.
- **Authentication**: Integration with modern auth patterns (Better Auth, JWT, Middleware-based protection).
- **Styling**: Mobile-first, utility-first design systems using **Tailwind CSS**.
- **Performance**: Optimization of Core Web Vitals through image optimization, font preloading, and aggressive caching strategies.

## Best Practices
1.  **Server-First**: Fetch data in Server Components at the layout or page level whenever possible.
2.  **Strict Typing**: Use TypeScript for all components and API interactions.
3.  **Boundary Management**: Implement clear Error Boundaries and Loading Skeletons for every route.
4.  **Colocation**: Keep components, hooks, and types as close to the route that uses them as possible (`/app/...`).
5.  **Optimistic UI**: Use `useOptimistic` for task CRUD operations to ensure a snappy user experience.

## Example Command
> "Initialize a new Next.js Phase-2 structure with a dashboard layout, server-side task fetching, and a client-side filter component."
