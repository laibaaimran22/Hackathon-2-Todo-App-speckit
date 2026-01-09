"use client";

import { Todo } from "@/types";
import { TodoDataSection } from "./TodoDataSection";

interface ClientTodoDataSectionProps {
  todos: Todo[];
}

export function ClientTodoDataSection({ todos }: ClientTodoDataSectionProps) {
  // Pass the todos as props to the client component
  return <TodoDataSection todos={todos} />;
}