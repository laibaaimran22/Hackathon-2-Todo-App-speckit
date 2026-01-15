"use client";

import { useState, useEffect } from "react";
import { Todo } from "@/types";
import { TodoList } from "./TodoList";
import { apiClient } from "@/lib/api-client";
import { TodoSkeleton } from "../ui/Skeleton";

interface ClientTodoSectionProps {
  token: string;
}

export function ClientTodoSection({ token }: ClientTodoSectionProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        setLoading(true);
        const fetchedTodos = await apiClient<Todo[]>("/api/tasks", {
          headers: {
            "Authorization": `Bearer ${token}`
          },
          next: { revalidate: 0 }
        });
        setTodos(fetchedTodos);
      } catch (err) {
        console.error("Failed to fetch todos:", err);
        setError("Failed to load tasks. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchTodos();
    }
  }, [token]);

  if (error) {
    return <div className="p-4 text-red-500 bg-red-50 rounded-lg">{error}</div>;
  }

  return (
    <>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-brand-slate">Your Tasks</h2>
        <span className="bg-brand-indigo/10 text-brand-indigo text-xs font-bold px-2 py-1 rounded-full">
          {todos.length} Total
        </span>
      </div>
      {loading ? <TodoSkeleton /> : <TodoList initialTodos={todos} />}
    </>
  );
}