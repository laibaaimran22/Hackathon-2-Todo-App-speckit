"use client";

import { useState } from "react";
import { Todo } from "@/types";
import { CheckCircle2, Circle, Trash2, Edit3, Clock, Sparkles, Calendar, Tag, Repeat } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { EditTodoModal } from "./EditTodoModal";
import { DeleteConfirmDialog } from "./DeleteConfirmDialog";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: number, completed: boolean) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onEdit: (id: number, title: string, description?: string, priority?: string, due_date?: string, recurrence_pattern?: string, tag_names?: string[]) => Promise<void>;
}

export function TodoItem({ todo, onToggle, onDelete, onEdit }: TodoItemProps) {
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const handleToggle = async () => {
    setIsAnimating(true);
    await onToggle(todo.id, !todo.is_completed);
    setTimeout(() => setIsAnimating(false), 300);
  };

  const handleEditSave = async (title: string, description: string, priority: string, due_date: string, recurrence_pattern: string, tag_names: string[]) => {
    await onEdit(todo.id, title, description || undefined, priority, due_date, recurrence_pattern, tag_names);
  };

  const handleDeleteConfirm = async () => {
    await onDelete(todo.id);
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    // Format using Pakistan timezone
    const pakistanTime = new Intl.DateTimeFormat('en-US', {
      timeZone: 'Asia/Karachi',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);

    // Calculate relative time using Pakistan timezone
    const now = new Date();
    const dateInPK = new Date(date.toLocaleString("en-US", {timeZone: "Asia/Karachi"}));
    const nowInPK = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Karachi"}));

    const diffMs = nowInPK.getTime() - dateInPK.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return pakistanTime;
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-500/20 text-red-300 border-red-400/30';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-300 border-yellow-400/30';
      case 'low':
        return 'bg-green-500/20 text-green-300 border-green-400/30';
      default:
        return 'bg-gray-500/20 text-gray-300 border-gray-400/30';
    }
  };

  const isOverdue = todo.due_date && new Date(todo.due_date) < new Date() && !todo.is_completed;

  return (
    <>
      <div
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className={cn(
          "group relative backdrop-blur-xl rounded-2xl border transition-all duration-300",
          todo.is_completed
            ? "bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border-emerald-400/30"
            : isOverdue
            ? "bg-gradient-to-br from-red-500/10 to-rose-500/10 border-red-400/30"
            : "bg-white/5 border-white/10 hover:border-white/20 hover:bg-white/10"
        )}
      >
        {/* Glow effect on hover */}
        {isHovered && !todo.is_completed && !isOverdue && (
          <div className="absolute inset-0 bg-gradient-to-r from-primary-500/10 to-accent-500/10 rounded-2xl blur-xl"></div>
        )}

        <div className="relative p-5">
          <div className="flex items-start gap-4">
            {/* Completion Toggle */}
            <button
              onClick={handleToggle}
              className={cn(
                "flex-shrink-0 mt-1 transition-all duration-300 cursor-pointer group/check",
                todo.is_completed
                  ? "text-emerald-400"
                  : "text-white/30 hover:text-primary-400",
                isAnimating && "transform scale-110"
              )}
            >
              {todo.is_completed ? (
                <div className="relative">
                  <div className="absolute inset-0 bg-emerald-400/30 rounded-full blur-md"></div>
                  <CheckCircle2
                    size={28}
                    className="relative transition-transform group-hover/check:scale-110"
                    fill="currentColor"
                  />
                </div>
              ) : (
                <Circle
                  size={28}
                  className="transition-transform group-hover/check:scale-110"
                  strokeWidth={2}
                />
              )}
            </button>

            {/* Content */}
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <h3
                  className={cn(
                    "text-lg font-semibold transition-all duration-300 mb-1",
                    todo.is_completed
                      ? "text-white/50 line-through decoration-2"
                      : "text-white"
                  )}
                >
                  {todo.title}
                </h3>

                {/* Priority badge */}
                <span className={cn(
                  "inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border",
                  getPriorityColor(todo.priority)
                )}>
                  {todo.priority.charAt(0).toUpperCase()}
                </span>
              </div>

              {todo.description && (
                <p
                  className={cn(
                    "text-sm transition-all duration-300 mb-3",
                    todo.is_completed ? "text-white/40 line-through" : "text-white/60"
                  )}
                >
                  {todo.description}
                </p>
              )}

              <div className="flex items-center gap-3 flex-wrap">
                {/* Created date */}
                <div className="flex items-center gap-1.5 text-xs text-white/40">
                  <Clock size={13} />
                  <span>{formatDate(todo.created_at)}</span>
                </div>

                {/* Due date */}
                {todo.due_date && (
                  <div className="flex items-center gap-1.5 text-xs">
                    <Calendar size={12} className={isOverdue ? "text-red-400" : "text-white/40"} />
                    <span className={isOverdue ? "text-red-400" : "text-white/40"}>
                      {formatDate(todo.due_date)}
                      {isOverdue && " (OVERDUE)"}
                    </span>
                  </div>
                )}

                {/* Recurrence pattern */}
                {todo.recurrence_pattern && (
                  <div className="flex items-center gap-1.5 text-xs text-blue-300">
                    <Repeat size={12} />
                    <span>{todo.recurrence_pattern}</span>
                  </div>
                )}

                {/* Completed badge */}
                {todo.is_completed && (
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                    <Sparkles size={11} />
                    Completed
                  </span>
                )}

                {/* Tags */}
                {todo.tags && todo.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {todo.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-500/20 text-indigo-300 border border-indigo-400/30"
                      >
                        <Tag size={10} />
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Actions */}
            <div
              className={cn(
                "flex items-center gap-1 transition-opacity duration-300",
                isHovered ? "opacity-100" : "opacity-0"
              )}
            >
              <button
                onClick={() => setShowEditModal(true)}
                className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-white/70 hover:text-primary-400 hover:bg-primary-500/10 rounded-lg transition-all duration-200 border border-transparent hover:border-primary-400/30"
                title="Edit Task"
              >
                <Edit3 size={16} />
                <span className="hidden sm:inline">Edit</span>
              </button>
              <button
                onClick={() => setShowDeleteDialog(true)}
                className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-white/70 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all duration-200 border border-transparent hover:border-red-400/30"
                title="Delete Task"
              >
                <Trash2 size={16} />
                <span className="hidden sm:inline">Delete</span>
              </button>
            </div>
          </div>
        </div>

        {/* Completed Progress Bar */}
        {todo.is_completed && (
          <div className="h-1 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-b-2xl overflow-hidden">
            <div className="h-full bg-gradient-to-r from-emerald-400 to-teal-400 animate-gradient" />
          </div>
        )}
      </div>

      {/* Edit Modal - Updated to pass additional props */}
      <EditTodoModal
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        onSave={handleEditSave}
        todo={{
          id: todo.id,
          title: todo.title,
          description: todo.description || null,
          priority: todo.priority,
          due_date: todo.due_date || "",
          recurrence_pattern: todo.recurrence_pattern || "",
          tags: todo.tags || [],
        }}
      />

      {/* Delete Confirmation Dialog */}
      <DeleteConfirmDialog
        isOpen={showDeleteDialog}
        onClose={() => setShowDeleteDialog(false)}
        onConfirm={handleDeleteConfirm}
        taskTitle={todo.title}
      />
    </>
  );
}
