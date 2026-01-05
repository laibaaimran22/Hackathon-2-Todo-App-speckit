# Phase 2 Frontend: UI Design

## 1. Visual Style
- **Colors**:
  - Primary: Indigo (#4f46e5)
  - Success: Emerald (#10b981)
  - Danger: Rose (#f43f5e)
  - Background: Slate-50 (#f8fafc)
- **Typography**: Inter (optimized via `next/font`).
- **Icons**: Lucide React.

## 2. Layouts

### 2.1 Landing Page
- Minimalist hero section with "Get Started" call-to-action.
- Feature overview highlighting Phase 2 improvements (Web, Auth, Modern UI).

### 2.2 Auth Pages
- Center-aligned card for Login and Signup.
- Validation error states shown inline on inputs.

### 2.3 Dashboard (Main)
- **Header**: App Logo, User Profile/Logout.
- **Input Area**: Fixed or top-aligned input for rapid task creation.
- **Task List**: Scrollable list of cards.
- **Task Card**:
  - Left: Completion checkbox.
  - Center: Title and Priority badge.
  - Right: Delete (trash icon) and Edit (pencil icon) buttons.

## 3. Responsive Strategy
- **Mobile**: Single column, full-width buttons, large touch targets (44px).
- **Tablet/Desktop**: Max-width container (768px) centered to maintain legibility.

## 4. Interactions
- **Optimistic Updates**: Task title strikethrough and status toggle happens instantly.
- **Loading States**: Skeleton screens for initial load; button spinners for mutations.
- **Feedback**: Toast notifications for errors or success messages.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
