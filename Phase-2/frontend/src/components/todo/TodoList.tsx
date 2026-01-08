"use client";

import { useOptimistic, useTransition } from "react";
import { Todo } from "@/types";
import { TodoItem } from "./TodoItem";
import { toggleTodo, deleteTodo, updateTodo } from "@/app/actions/todo";
import { ListTodo, CheckCircle2 } from "lucide-react";

interface TodoListProps {
    initialTodos: Todo[];
}

export function TodoList({ initialTodos }: TodoListProps) {
    const [optimisticTodos, addOptimisticTodo] = useOptimistic(
        initialTodos,
        (state: Todo[], payload: { action: string; id: string; data?: any }) => {
            const { action, id, data } = payload;
            switch (action) {
                case "toggle":
                    return state.map((t) =>
                        t.id === id ? { ...t, is_completed: data?.is_completed } : t
                    );
                case "delete":
                    return state.filter((t) => t.id !== id);
                case "update":
                    return state.map((t) =>
                        t.id === id ? { ...t, title: data?.title, description: data?.description } : t
                    );
                case "add":
                    return [data, ...state];
                default:
                    return state;
            }
        }
    );

    const [isPending, startTransition] = useTransition();

    const handleToggle = async (id: string, is_completed: boolean) => {
        startTransition(async () => {
            addOptimisticTodo({ action: "toggle", id, data: { is_completed } });
            await toggleTodo(id, is_completed);
        });
    };

    const handleDelete = async (id: string) => {
        startTransition(async () => {
            addOptimisticTodo({ action: "delete", id });
            await deleteTodo(id);
        });
    };

    const handleEdit = async (id: string, title: string, description?: string) => {
        startTransition(async () => {
            addOptimisticTodo({ action: "update", id, data: { title, description } });
            await updateTodo(id, title, description);
        });
    };

    const completedCount = optimisticTodos.filter(t => t.is_completed).length;
    const pendingCount = optimisticTodos.length - completedCount;

    return (
        <div className={isPending ? "opacity-70 transition-opacity" : ""}>
            {/* Stats */}
            {optimisticTodos.length > 0 && (
                <div className="flex gap-4 mb-4">
                    <div className="flex items-center gap-2 text-sm">
                        <span className="w-2 h-2 rounded-full bg-indigo-500" />
                        <span className="text-gray-600">{pendingCount} pending</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                        <span className="w-2 h-2 rounded-full bg-green-500" />
                        <span className="text-gray-600">{completedCount} completed</span>
                    </div>
                </div>
            )}

            <div className="space-y-3">
                {optimisticTodos.length === 0 ? (
                    <div className="text-center py-16 px-6 bg-white rounded-2xl border-2 border-dashed border-gray-200">
                        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-indigo-50 to-purple-50 mb-5">
                            <ListTodo size={40} className="text-indigo-400" />
                        </div>
                        <h3 className="text-xl font-semibold text-gray-800 mb-2">
                            No tasks yet! 🎉
                        </h3>
                        <p className="text-gray-500 max-w-sm mx-auto">
                            Create your first task above and start being productive.
                        </p>
                        <div className="mt-6 flex items-center justify-center gap-2 text-sm text-gray-400">
                            <CheckCircle2 size={16} />
                            <span>Tasks will appear here</span>
                        </div>
                    </div>
                ) : (
                    optimisticTodos.map((todo) => (
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
