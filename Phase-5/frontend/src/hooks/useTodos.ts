'use client';

import { useState, useCallback } from 'react';
import { Todo } from '@/types';
import { addTodo as addTodoAction, updateTodo as updateTodoAction, deleteTodo as deleteTodoAction, toggleTodo as toggleTodoAction } from '@/app/actions/todo';
import { apiClient } from '@/lib/api-client';
import { getJwtToken } from '@/lib/auth-utils';

interface UseTodosOptions {
  initialTodos?: Todo[];
}

export function useTodos(options: UseTodosOptions = {}) {
  const [todos, setTodos] = useState<Todo[]>(options.initialTodos || []);
  const [loading, setLoading] = useState(false);

  const refreshTodos = useCallback(async () => {
    try {
      setLoading(true);

      // Get token for authentication
      const token = await getJwtToken();

      // Fetch todos directly from the API
      const fetchedTodos = await apiClient<Todo[]>('/api/tasks', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      setTodos(fetchedTodos);
    } catch (error) {
      console.error('Failed to refresh todos:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const addTodo = useCallback(async (
    title: string,
    description?: string,
    priority?: string,
    due_date?: string,
    recurrence_pattern?: string,
    tag_names?: string[]
  ) => {
    try {
      setLoading(true);

      // Execute server action with explicit args
      await addTodoAction(title, description, priority, due_date, recurrence_pattern, tag_names);

      // Refresh the todos list
      await refreshTodos();
    } catch (error) {
      console.error('Failed to add todo:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, [refreshTodos]);

  const updateTodo = useCallback(async (id: number, title: string, description?: string) => {
    try {
      setLoading(true);

      // Execute server action - this will trigger revalidation
      await updateTodoAction(id, title, description);

      // Update local state optimistically to avoid waiting for revalidation
      setTodos(prevTodos =>
        prevTodos.map(todo =>
          todo.id === id ? { ...todo, title, description: description || todo.description } : todo
        )
      );
    } catch (error) {
      console.error('Failed to update todo:', error);
      // If there's an error, refresh to sync with server state
      await refreshTodos();
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const removeTodo = useCallback(async (id: number) => {
    try {
      setLoading(true);

      // Execute server action - this will trigger revalidation
      await deleteTodoAction(id);

      // Update local state optimistically to avoid waiting for revalidation
      setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
    } catch (error) {
      console.error('Failed to delete todo:', error);
      // If there's an error, refresh to sync with server state
      await refreshTodos();
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const toggleTodoCompletion = useCallback(async (id: number) => {
    try {
      setLoading(true);

      // Find the current todo to get its current completion status
      const currentTodo = todos.find(todo => todo.id === id);
      if (!currentTodo) {
        throw new Error('Todo not found');
      }

      // Execute server action - this will trigger revalidation
      await toggleTodoAction(id, !currentTodo.is_completed);

      // Update local state optimistically to avoid waiting for revalidation
      setTodos(prevTodos =>
        prevTodos.map(todo =>
          todo.id === id ? { ...todo, is_completed: !currentTodo.is_completed } : todo
        )
      );
    } catch (error) {
      console.error('Failed to toggle todo:', error);
      // If there's an error, refresh to sync with server state
      await refreshTodos();
      throw error;
    } finally {
      setLoading(false);
    }
  }, [todos]);

  return {
    todos,
    loading,
    addTodo,
    updateTodo,
    removeTodo,
    toggleTodoCompletion,
    refreshTodos,
  };
}
