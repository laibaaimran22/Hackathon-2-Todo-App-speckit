"use client";

import { useOptimistic, useTransition } from "react";
import { useRouter } from "next/navigation";
import { Todo } from "@/types";
import { TodoItem } from "./TodoItem";
import { toggleTodo as toggleTodoAction, deleteTodo as deleteTodoAction, updateTodo as updateTodoAction } from "@/app/actions/todo";
import { ListTodo, CheckCircle2 } from "lucide-react";

interface TodoListProps {
    initialTodos: Todo[];
    updateTodo?: (id: number, title: string, description?: string) => Promise<void>;
    removeTodo?: (id: number) => Promise<void>;
    toggleTodoCompletion?: (id: number) => Promise<void>;
}

export function TodoList({ initialTodos, updateTodo, removeTodo, toggleTodoCompletion }: TodoListProps) {
    const router = useRouter();
    type OptimisticAction =
        | { action: 'toggle'; id: number; data: { is_completed: boolean } }
        | { action: 'delete'; id: number }
        | { action: 'update'; id: number; data: { title?: string; description?: string } }
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
                        t.id === Number(action.id) ? { ...t, title: action.data.title ?? t.title, description: action.data.description ?? t.description } : t
                    );
                case "add":
                    return [action.data, ...state];
            }
        }
    );

    const [isPending, startTransition] = useTransition();

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

    const handleEdit = async (id: number, title: string, description?: string) => {
        startTransition(async () => {
            // Apply optimistic update to provide immediate feedback
            addOptimisticTodo({ action: 'update', id, data: { title, description } });

            try {
                if (updateTodo) {
                    // Use parent function if provided (for chatbot integration)
                    await updateTodo(id, title, description);
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