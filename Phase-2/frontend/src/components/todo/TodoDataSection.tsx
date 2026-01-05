"use client";

import { useState } from "react";
import { Todo } from "@/types";
import { TodoList } from "./TodoList";
import { ListTodo, Clock, Trophy, CheckCircle2, TrendingUp } from "lucide-react";

type FilterType = 'all' | 'pending' | 'completed';

interface TodoDataSectionProps {
  todos: Todo[];
}

export function TodoDataSection({ todos }: TodoDataSectionProps) {
  const [filter, setFilter] = useState<FilterType>('all');

  const filteredTodos = todos.filter(todo => {
    if (filter === 'pending') return !todo.is_completed;
    if (filter === 'completed') return todo.is_completed;
    return true;
  });

  const completedCount = todos.filter(t => t.is_completed).length;
  const pendingCount = todos.length - completedCount;
  const progress = todos.length > 0 ? Math.round((completedCount / todos.length) * 100) : 0;

  return (
    <div>
      {/* Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-5 text-white shadow-lg shadow-indigo-500/25">
          <div className="flex items-center justify-between mb-3">
            <ListTodo className="w-6 h-6 text-white/80" />
            <span className="text-3xl font-bold">{todos.length}</span>
          </div>
          <p className="text-white/80 text-sm font-medium">Total Tasks</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <Clock className="w-6 h-6 text-amber-500" />
            <span className="text-3xl font-bold text-gray-800">{pendingCount}</span>
          </div>
          <p className="text-gray-500 text-sm font-medium">Pending</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <CheckCircle2 className="w-6 h-6 text-green-500" />
            <span className="text-3xl font-bold text-gray-800">{completedCount}</span>
          </div>
          <p className="text-gray-500 text-sm font-medium">Completed</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <TrendingUp className="w-6 h-6 text-violet-500" />
            <span className="text-3xl font-bold text-gray-800">{progress}%</span>
          </div>
          <p className="text-gray-500 text-sm font-medium">Progress</p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 mb-6">
        {[
          { key: 'all', label: 'All Tasks', icon: ListTodo, count: todos.length },
          { key: 'pending', label: 'Pending', icon: Clock, count: pendingCount },
          { key: 'completed', label: 'Completed', icon: Trophy, count: completedCount },
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key as FilterType)}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-medium transition-all duration-200 ${
              filter === tab.key
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25'
                : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
            <span className={`px-2 py-0.5 rounded-full text-xs ${
              filter === tab.key ? 'bg-white/20' : 'bg-gray-100'
            }`}>
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Todo List */}
      <TodoList initialTodos={filteredTodos} />
    </div>
  );
}
