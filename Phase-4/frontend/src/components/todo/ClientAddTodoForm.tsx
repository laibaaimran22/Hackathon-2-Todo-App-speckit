"use client";

import { AddTodoForm } from "./AddTodoForm";

interface ClientAddTodoFormProps {
  onAddTodo?: (title: string, description?: string) => Promise<void>;
}

export function ClientAddTodoForm({ onAddTodo }: ClientAddTodoFormProps) {
  // Simple wrapper for AddTodoForm - pass down props if needed
  return <AddTodoForm onAddTodo={onAddTodo} />;
}