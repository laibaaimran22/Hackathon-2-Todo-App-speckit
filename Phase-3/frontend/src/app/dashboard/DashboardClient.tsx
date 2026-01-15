'use client';

import { Suspense, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { ClientAddTodoForm } from '@/components/todo/ClientAddTodoForm';
import { ClientSignOutButton } from '@/components/auth/ClientSignOutButton';
import { ClientTodoDataSection } from '@/components/todo/ClientTodoDataSection';
import { Todo } from '@/types';
import { ChatBotIcon } from '@/components/chat/ChatBotIcon';
import { ChatWindow } from '@/components/chat/ChatWindow';
import { useChatBot } from '@/hooks/useChatBot';
import { useTodos } from '@/hooks/useTodos';
import {
  CheckCircle2,
  ListTodo,
  Plus,
  Sparkles,
  TrendingUp,
} from 'lucide-react';

interface DashboardClientProps {
  userEmail: string;
  todos: Todo[];
}

export function DashboardClient({ userEmail, todos: initialTodos }: DashboardClientProps) {
  const { todos, loading, addTodo, updateTodo, removeTodo, toggleTodoCompletion, refreshTodos } = useTodos({ initialTodos });
  const completedCount = todos.filter(t => t.is_completed).length;
  const pendingCount = todos.length - completedCount;
  const userInitial = userEmail.charAt(0).toUpperCase();
  const userName = userEmail.split('@')[0];

  // Chatbot state and logic
  const [isChatOpen, setIsChatOpen] = useState(false);
  const { messages, isLoading, sendMessage } = useChatBot(todos, refreshTodos);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary-500/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-primary-500/5 via-transparent to-transparent rounded-full"></div>
      </div>

      {/* Header */}
      <header className="relative z-10 backdrop-blur-xl bg-white/5 border-b border-white/10 sticky top-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            {/* Logo & Brand */}
            <div className="flex items-center gap-4">
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-accent-500 rounded-2xl blur-lg group-hover:blur-xl transition-all opacity-75"></div>
                <div className="relative w-12 h-12 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                  <CheckCircle2 className="w-7 h-7 text-white" strokeWidth={2.5} />
                </div>
              </div>
              <div className="hidden sm:block">
                <h1 className="text-xl font-bold bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">
                  Todo Evolution
                </h1>
                <p className="text-xs text-white/50">Phase 3 • AI Chatbot</p>
              </div>
            </div>

            {/* User Section */}
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex items-center gap-3 px-4 py-2.5 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20">
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                  <span className="text-white font-bold text-sm">{userInitial}</span>
                </div>
                <span className="text-sm font-medium text-white/90">{userName}</span>
              </div>
              <ClientSignOutButton />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Section with Stats */}
        <div className="mb-12">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            {/* Welcome Text */}
            <div>
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-3 flex items-center gap-3">
                <Sparkles className="w-10 h-10 text-primary-400" />
                Welcome back, {userName}!
              </h2>
              <p className="text-lg text-white/60">
                Let&apos;s make today productive and achieve your goals
              </p>
            </div>

            {/* Stats Cards */}
            <div className="flex gap-4">
              <div className="backdrop-blur-xl bg-gradient-to-br from-primary-500/15 to-primary-600/15 border border-primary-400/20 rounded-2xl p-4 min-w-[120px]">
                <div className="text-3xl font-bold bg-gradient-to-br from-primary-400 to-primary-500 bg-clip-text text-transparent mb-1">{pendingCount}</div>
                <div className="text-sm text-white/70">Pending</div>
              </div>
              <div className="backdrop-blur-xl bg-gradient-to-br from-accent-500/15 to-accent-600/15 border border-accent-400/20 rounded-2xl p-4 min-w-[120px]">
                <div className="text-3xl font-bold bg-gradient-to-br from-accent-400 to-accent-500 bg-clip-text text-transparent mb-1">{completedCount}</div>
                <div className="text-sm text-white/70">Completed</div>
              </div>
              <div className="backdrop-blur-xl bg-gradient-to-br from-blue-500/15 to-blue-600/15 border border-blue-400/20 rounded-2xl p-4 min-w-[120px]">
                <div className="text-3xl font-bold bg-gradient-to-br from-blue-400 to-blue-500 bg-clip-text text-transparent mb-1">{todos.length}</div>
                <div className="text-sm text-white/70">Total</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Column - Tasks */}
          <div className="lg:col-span-2 space-y-6">
            {/* Tasks Section */}
            <section>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center backdrop-blur-xl shadow-lg shadow-primary-500/25">
                  <ListTodo className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-white">Your Tasks</h3>
                <div className="ml-auto">
                  <span className="px-3 py-1 rounded-full text-xs font-semibold bg-white/10 text-white/80 backdrop-blur-xl border border-white/20">
                    {todos.length} {todos.length === 1 ? 'task' : 'tasks'}
                  </span>
                </div>
              </div>

              <Suspense fallback={
                <div className="space-y-4">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="p-6 backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl flex items-center gap-4 animate-pulse">
                      <div className="w-6 h-6 rounded-full bg-white/20" />
                      <div className="flex-1 h-6 bg-white/20 rounded" />
                      <div className="w-24 h-6 bg-white/20 rounded" />
                    </div>
                  ))}
                </div>
              }>
                <ClientTodoDataSection
                  todos={todos}
                  updateTodo={updateTodo}
                  removeTodo={removeTodo}
                  toggleTodoCompletion={toggleTodoCompletion}
                />
              </Suspense>
            </section>
          </div>

          {/* Sidebar - Add Task */}
          <div className="lg:col-span-1">
            <div className="sticky top-24">
              <section className="backdrop-blur-xl bg-gradient-to-br from-white/10 to-white/5 border border-white/20 rounded-3xl p-6 shadow-2xl">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-500 to-accent-600 flex items-center justify-center shadow-lg shadow-accent-500/25">
                    <Plus className="w-5 h-5 text-white" strokeWidth={2.5} />
                  </div>
                  <h3 className="text-xl font-bold text-white">Add New Task</h3>
                </div>
                <ClientAddTodoForm onAddTodo={addTodo} />

                {/* Quick Stats */}
                <div className="mt-8 pt-6 border-t border-white/10">
                  <h4 className="text-sm font-semibold text-white/70 mb-4 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" />
                    Today&apos;s Progress
                  </h4>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-white/60">Completion Rate</span>
                      <span className="text-sm font-semibold text-white">
                        {todos.length > 0 ? Math.round((completedCount / todos.length) * 100) : 0}%
                      </span>
                    </div>
                    <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full transition-all duration-500 shadow-lg shadow-primary-500/50"
                        style={{ width: `${todos.length > 0 ? (completedCount / todos.length) * 100 : 0}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </div>
        </div>

        {/* Chatbot Components */}
        <ChatBotIcon
          onOpen={() => setIsChatOpen(true)}
          unreadCount={messages.length}
        />
        <ChatWindow
          isOpen={isChatOpen}
          onClose={() => setIsChatOpen(false)}
          onSendMessage={sendMessage}
          messages={messages}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
}