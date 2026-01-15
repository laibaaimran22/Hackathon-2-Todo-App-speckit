'use client';

import { createContext, useContext, ReactNode } from 'react';
import { Todo } from '@/types';

interface TodosContextType {
  todos: Todo[];
  refreshTodos: () => Promise<void>;
  loading: boolean;
}

const TodosContext = createContext<TodosContextType | undefined>(undefined);

export function TodosProvider({
  children,
  initialTodos
}: {
  children: ReactNode;
  initialTodos: Todo[];
}) {
  // In a real implementation, this would use the useTodos hook
  // For now, I'll implement a simplified version

  const refreshTodos = async () => {
    // This would be implemented in the actual hook
  };

  const contextValue: TodosContextType = {
    todos: initialTodos,
    refreshTodos,
    loading: false,
  };

  return (
    <TodosContext.Provider value={contextValue}>
      {children}
    </TodosContext.Provider>
  );
}

export function useTodosContext() {
  const context = useContext(TodosContext);
  if (context === undefined) {
    throw new Error('useTodosContext must be used within a TodosProvider');
  }
  return context;
}