'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { MessageCircle, Bot } from 'lucide-react';

interface ChatBotIconProps {
  onOpen: () => void;
  unreadCount?: number;
}

export function ChatBotIcon({ onOpen, unreadCount = 0 }: ChatBotIconProps) {
  return (
    <Button
      onClick={onOpen}
      className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 hover:from-primary-600 hover:to-accent-600 shadow-lg shadow-primary-500/30 hover:shadow-primary-500/50 flex items-center justify-center z-40"
      aria-label="Open chatbot"
    >
      <div className="relative">
        <Bot className="w-6 h-6 text-white" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </div>
    </Button>
  );
}