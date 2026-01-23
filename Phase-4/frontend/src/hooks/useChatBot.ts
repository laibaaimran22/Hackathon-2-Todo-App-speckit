'use client';

import { useState, useCallback } from 'react';
import { Todo } from '@/types';
import { CohereClient } from '@/lib/cohere-client';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export function useChatBot(initialTodos: Todo[], onRefresh?: () => void) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [todos, setTodos] = useState<Todo[]>(initialTodos);
  const cohereClient = new CohereClient();

  const addMessage = useCallback((role: 'user' | 'assistant', content: string) => {
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date()
    }]);
  }, []);

  const processMessage = useCallback(async (message: string) => {
    setIsLoading(true);

    try {
      // Get the JWT token for authentication using a client-side API route that handles session verification
      const response = await fetch('/api/token');
      if (!response.ok) {
        throw new Error('Failed to retrieve authentication token');
      }

      const { token } = await response.json();
      if (!token) {
        throw new Error('No authentication token available');
      }

      // Process the message using Cohere
      const cohereResponse = await cohereClient.chat(message, todos, token);
      addMessage('assistant', cohereResponse.text);

      // Update todos if the response includes changes
      if (cohereResponse.todos) {
        setTodos(cohereResponse.todos);
      }

      // Trigger refresh to ensure dashboard state is consistent
      if (onRefresh) {
        onRefresh();
      }
    } catch (error) {
      console.error('Error processing message:', error);
      addMessage('assistant', 'Sorry, I encountered an error processing your request. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [addMessage, todos, cohereClient, onRefresh]);

  const sendMessage = useCallback(async (message: string) => {
    addMessage('user', message);
    await processMessage(message);
  }, [addMessage, processMessage]);

  return {
    messages,
    isLoading,
    todos,
    sendMessage,
    setTodos
  };
}