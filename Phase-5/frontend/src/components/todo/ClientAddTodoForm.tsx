"use client";

import { AddTodoForm } from "./AddTodoForm";

interface ClientAddTodoFormProps {
  onAddTodo?: (
    title: string,
    description?: string,
    priority?: string,
    due_date?: string,
    recurrence_pattern?: string,
    tag_names?: string[]
  ) => Promise<void>;
}

export function ClientAddTodoForm({ onAddTodo }: ClientAddTodoFormProps) {
  // Simple wrapper for AddTodoForm - pass down props if needed
  return <AddTodoForm onAddTodo={onAddTodo} />;
}
