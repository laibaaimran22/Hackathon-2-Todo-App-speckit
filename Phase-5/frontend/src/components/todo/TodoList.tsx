"use client";

import { useOptimistic, useTransition, useState } from "react";
import { useRouter } from "next/navigation";
import { Todo } from "@/types";
import { TodoItem } from "./TodoItem";
import { toggleTodo as toggleTodoAction, deleteTodo as deleteTodoAction, updateTodo as updateTodoAction } from "@/app/actions/todo";
import { ListTodo, CheckCircle2, Filter, X } from "lucide-react";

interface TodoListProps {
    initialTodos: Todo[];
    updateTodo?: (id: number, title: string, description?: string, priority?: string, due_date?: string, recurrence_pattern?: string, tag_names?: string[]) => Promise<void>;
    removeTodo?: (id: number) => Promise<void>;
    toggleTodoCompletion?: (id: number) => Promise<void>;
}

export function TodoList({ initialTodos, updateTodo, removeTodo, toggleTodoCompletion }: TodoListProps) {
    const router = useRouter();
    type OptimisticAction =
        | { action: 'toggle'; id: number; data: { is_completed: boolean } }
        | { action: 'delete'; id: number }
        | { action: 'update'; id: number; data: { title?: string; description?: string; priority?: string; due_date?: string; recurrence_pattern?: string; tag_names?: string[] } }
        | { action: 'add'; data: Todo };

    const [optimisticTodos, addOptimisticTodo] = useOptimistic(
        initialTodos,
        (state: Todo[], action: OptimisticAction): Todo[] => {
            switch (action.action) {
                case "toggle":
                    return state.map((t) =>
                        t.id === Number(action.id) ? { ...t, is_completed: action.data.is_completed } : t
                    );
                case "delete":
                    return state.filter((t) => t.id !== Number(action.id));
                case "update":
                    return state.map((t) =>
                        t.id === Number(action.id) ? {
                            ...t,
                            title: action.data.title ?? t.title,
                            description: action.data.description ?? t.description,
                            priority: action.data.priority ?? t.priority,
                            due_date: action.data.due_date ?? t.due_date,
                            recurrence_pattern: action.data.recurrence_pattern ?? t.recurrence_pattern,
                            tags: action.data.tag_names ?? t.tags
                        } : t
                    );
                case "add":
                    return [action.data, ...state];
            }
        }
    );

    const [isPending, startTransition] = useTransition();

    // Filtering states
    const [filterStatus, setFilterStatus] = useState<'all' | 'completed' | 'pending'>('all');
    const [filterPriority, setFilterPriority] = useState<string>('all');
    const [filterTag, setFilterTag] = useState<string>('all');

    // Get all unique tags from todos
    const allTags = Array.from(new Set(optimisticTodos.flatMap(todo => todo.tags)));

    // Apply filters
    const filteredTodos = optimisticTodos.filter(todo => {
        const statusMatch = filterStatus === 'all' ||
                          (filterStatus === 'completed' && todo.is_completed) ||
                          (filterStatus === 'pending' && !todo.is_completed);

        const priorityMatch = filterPriority === 'all' || todo.priority === filterPriority;

        const tagMatch = filterTag === 'all' || todo.tags.includes(filterTag);

        return statusMatch && priorityMatch && tagMatch;
    });

    const handleToggle = async (id: number, is_completed: boolean) => {
        startTransition(async () => {
            // Apply optimistic update to provide immediate feedback
            addOptimisticTodo({ action: 'toggle', id, data: { is_completed: !is_completed } });

            try {
                if (toggleTodoCompletion) {
                    // Use parent function if provided (for chatbot integration)
                    await toggleTodoCompletion(id);
                } else {
                    // Direct server action call like in Phase 2
                    await toggleTodoAction(id, !is_completed);
                    // No need to refresh since optimistic update is immediate and server action handles revalidation
                }
            } catch (error) {
                console.error('Failed to toggle task:', error);
                // If the task was not found, refresh to sync with server state
                if (error instanceof Error && error.message.includes("Task not found")) {
                    router.refresh();
                } else {
                    router.refresh(); // Refresh to sync with server state
                }
            }
        });
    };

    const handleDelete = async (id: number) => {
        startTransition(async () => {
            // Apply optimistic update to provide immediate feedback
            addOptimisticTodo({ action: 'delete', id });

            try {
                if (removeTodo) {
                    // Use parent function if provided (for chatbot integration)
                    await removeTodo(id);
                } else {
                    // Direct server action call like in Phase 2
                    await deleteTodoAction(id);
                    // No need to refresh since optimistic update is immediate and server action handles revalidation
                }
            } catch (error) {
                console.error('Failed to delete task:', error);
                // If the task was already deleted, that's fine - just refresh to sync with server state
                if (error instanceof Error && error.message.includes("Task not found")) {
                    // Task was already deleted, just refresh to sync with server state
                    router.refresh();
                } else {
                    // For other errors, refresh to sync with server state
                    router.refresh();
                }
            }
        });
    };

    const handleEdit = async (id: number, title: string, description?: string, priority?: string, due_date?: string, recurrence_pattern?: string, tag_names?: string[]) => {
        startTransition(async () => {
            // Apply optimistic update to provide immediate feedback
            addOptimisticTodo({ action: 'update', id, data: { title, description, priority, due_date, recurrence_pattern, tag_names } });

            try {
                if (updateTodo) {
                    // Use parent function if provided (for chatbot integration)
                    await updateTodo(id, title, description, priority, due_date, recurrence_pattern, tag_names);
                } else {
                    // Direct server action call like in Phase 2
                    await updateTodoAction(id, title, description);
                    // No need to refresh since optimistic update is immediate and server action handles revalidation
                }
            } catch (error) {
                console.error('Failed to update task:', error);
                // If the task was not found (likely already deleted), refresh to sync with server state
                if (error instanceof Error && (error.message.includes("Task not found") || error.message.includes("404"))) {
                    router.refresh();
                } else {
                    router.refresh(); // Refresh to sync with server state
                }
            }
        });
    };

    const completedCount = filteredTodos.filter(t => t.is_completed).length;
    const pendingCount = filteredTodos.length - completedCount;

    return (
        <div className={isPending ? "opacity-70 transition-opacity" : ""}>
            {/* Filter Controls */}
            {(optimisticTodos.length > 0) && (
                <div className="mb-6 p-4 bg-white/5 backdrop-blur-xl rounded-xl border border-white/10">
                    <div className="flex flex-wrap gap-4 items-center">
                        <div className="flex items-center gap-2 text-sm text-white/70">
                            <Filter size={16} />
                            <span>Filters:</span>
                        </div>

                        {/* Status Filter */}
                        <div className="flex items-center gap-2">
                            <label className="text-sm text-white/60">Status:</label>
                            <select
                                value={filterStatus}
                                onChange={(e) => setFilterStatus(e.target.value as 'all' | 'completed' | 'pending')}
                                className="px-3 py-1.5 rounded-lg bg-slate-900/70 border border-white/20 text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            >
                                <option value="all" className="bg-slate-900 text-white">All</option>
                                <option value="pending" className="bg-slate-900 text-white">Pending</option>
                                <option value="completed" className="bg-slate-900 text-white">Completed</option>
                            </select>
                        </div>

                        {/* Priority Filter */}
                        <div className="flex items-center gap-2">
                            <label className="text-sm text-white/60">Priority:</label>
                            <select
                                value={filterPriority}
                                onChange={(e) => setFilterPriority(e.target.value)}
                                className="px-3 py-1.5 rounded-lg bg-slate-900/70 border border-white/20 text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            >
                                <option value="all" className="bg-slate-900 text-white">All</option>
                                <option value="high" className="bg-slate-900 text-white">High</option>
                                <option value="medium" className="bg-slate-900 text-white">Medium</option>
                                <option value="low" className="bg-slate-900 text-white">Low</option>
                            </select>
                        </div>

                        {/* Tag Filter */}
                        <div className="flex items-center gap-2">
                            <label className="text-sm text-white/60">Tag:</label>
                            <select
                                value={filterTag}
                                onChange={(e) => setFilterTag(e.target.value)}
                                className="px-3 py-1.5 rounded-lg bg-slate-900/70 border border-white/20 text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            >
                                <option value="all" className="bg-slate-900 text-white">All</option>
                                {allTags.map((tag, index) => (
                                    <option key={index} value={tag} className="bg-slate-900 text-white">{tag}</option>
                                ))}
                            </select>
                        </div>

                        {/* Reset Filters Button */}
                        {(filterStatus !== 'all' || filterPriority !== 'all' || filterTag !== 'all') && (
                            <button
                                onClick={() => {
                                    setFilterStatus('all');
                                    setFilterPriority('all');
                                    setFilterTag('all');
                                }}
                                className="flex items-center gap-1 px-3 py-1.5 text-sm text-white/70 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                            >
                                <X size={14} />
                                <span>Reset</span>
                            </button>
                        )}
                    </div>
                </div>
            )}

            {/* Stats */}
            {filteredTodos.length > 0 && (
                <div className="flex gap-4 mb-4">
                    <div className="flex items-center gap-2 text-sm">
                        <span className="w-2 h-2 rounded-full bg-indigo-500" />
                        <span className="text-white/60">{pendingCount} pending</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                        <span className="w-2 h-2 rounded-full bg-green-500" />
                        <span className="text-white/60">{completedCount} completed</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                        <span className="w-2 h-2 rounded-full bg-blue-500" />
                        <span className="text-white/60">{filteredTodos.length} total</span>
                    </div>
                </div>
            )}

            <div className="space-y-3">
                {filteredTodos.length === 0 ? (
                    <div className="text-center py-16 px-6 bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10">
                        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-indigo-500/20 to-purple-500/20 mb-5">
                            <ListTodo size={40} className="text-indigo-400" />
                        </div>
                        <h3 className="text-xl font-semibold text-white mb-2">
                            No tasks found! 🎉
                        </h3>
                        <p className="text-white/60 max-w-sm mx-auto">
                            {optimisticTodos.length === 0
                                ? "Create your first task above and start being productive."
                                : "Try adjusting your filters to see more tasks."
                            }
                        </p>
                        <div className="mt-6 flex items-center justify-center gap-2 text-sm text-white/40">
                            <CheckCircle2 size={16} />
                            <span>Tasks will appear here</span>
                        </div>
                    </div>
                ) : (
                    filteredTodos.map((todo) => (
                        <TodoItem
                            key={todo.id}
                            todo={todo}
                            onToggle={handleToggle}
                            onDelete={handleDelete}
                            onEdit={handleEdit}
                        />
                    ))
                )}
            </div>
        </div>
    );
}
