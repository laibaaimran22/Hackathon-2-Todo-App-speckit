"use client";

import { Todo } from "@/types";
import { TodoDataSection } from "./TodoDataSection";

interface ClientTodoDataSectionProps {
  todos: Todo[];
  updateTodo?: (id: number, title: string, description?: string) => Promise<void>;
  removeTodo?: (id: number) => Promise<void>;
  toggleTodoCompletion?: (id: number) => Promise<void>;
}

export function ClientTodoDataSection({ todos, updateTodo, removeTodo, toggleTodoCompletion }: ClientTodoDataSectionProps) {
  // Pass the todos and functions as props to the client component
  return <TodoDataSection todos={todos} updateTodo={updateTodo} removeTodo={removeTodo} toggleTodoCompletion={toggleTodoCompletion} />;
}