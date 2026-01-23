'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Send, Bot, X, MessageCircle } from 'lucide-react';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
  onSendMessage: (message: string) => void;
  messages: ChatMessage[];
  isLoading: boolean;
}

export function ChatWindow({
  isOpen,
  onClose,
  onSendMessage,
  messages,
  isLoading
}: ChatWindowProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-24 right-6 w-96 h-96 bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl shadow-2xl shadow-black/50 flex flex-col z-50 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/10 bg-gradient-to-r from-primary-500/20 to-accent-500/20">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-primary-400" />
          <span className="font-semibold text-white">Todo Assistant</span>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={onClose}
          className="text-white/70 hover:text-white hover:bg-white/10"
        >
          <X className="w-4 h-4" />
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-2xl ${
                message.role === 'user'
                  ? 'bg-primary-500 text-white rounded-br-md'
                  : 'bg-white/10 text-white rounded-bl-md'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white/10 text-white p-3 rounded-2xl rounded-bl-md max-w-[80%]">
              <div className="flex items-center gap-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
                <span className="text-xs">Thinking...</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-white/10 bg-white/5">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask me to manage your tasks..."
            className="flex-1 bg-white/10 text-white placeholder-white/50 px-3 py-2 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isLoading}
          />
          <Button
            type="submit"
            size="sm"
            disabled={!inputValue.trim() || isLoading}
            className="bg-primary-500 hover:bg-primary-600 text-white"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </form>
    </div>
  );
}