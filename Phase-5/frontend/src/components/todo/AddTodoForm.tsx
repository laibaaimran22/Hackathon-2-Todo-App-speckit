"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, Loader2, Sparkles, X, Calendar, Tag, Repeat } from "lucide-react";
import { apiClient } from "@/lib/api-client";
import { getJwtToken } from "@/lib/auth-utils";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface AddTodoFormProps {
  onAddTodo?: (title: string, description?: string, priority?: string, due_date?: string, recurrence_pattern?: string, tag_names?: string[]) => Promise<void>;
}

export function AddTodoForm({ onAddTodo }: AddTodoFormProps = {}) {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("medium");
  const [dueDate, setDueDate] = useState("");
  const [recurrencePattern, setRecurrencePattern] = useState("");
  const [tags, setTags] = useState("");
  const [isPending, setIsPending] = useState(false);
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsPending(true);
    try {
      const tagArray = tags.split(",").map(tag => tag.trim()).filter(tag => tag);

      if (onAddTodo) {
        // Use the passed function
        await onAddTodo(
          title.trim(),
          description.trim() || undefined,
          priority,
          dueDate,
          recurrencePattern,
          tagArray
        );
      } else {
        // Direct API call for immediate update
        const token = await getJwtToken();
        await apiClient("/api/tasks", {
          method: "POST",
          body: JSON.stringify({
            title: title.trim(),
            description: description.trim() || undefined,
            priority,
            due_date: dueDate || undefined,
            recurrence_pattern: recurrencePattern || undefined,
            tag_names: tagArray
          }),
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        router.refresh(); // Refresh to get updated data from server
      }

      setTitle("");
      setDescription("");
      setPriority("medium");
      setDueDate("");
      setRecurrencePattern("");
      setTags("");
      setShowAdvancedOptions(false);
    } catch (error) {
      console.error("Failed to add todo:", error);
      router.refresh(); // Refresh to sync with server state
    } finally {
      setIsPending(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-3">
        <div className="relative">
          <input
            type="text"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (e.target.value.trim() && !showAdvancedOptions) {
                setShowAdvancedOptions(true);
              }
            }}
            placeholder="What needs to be done?"
            className="w-full px-4 py-3.5 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all text-white placeholder:text-white/40 text-base"
            disabled={isPending}
          />
          {title.trim() && (
            <button
              type="button"
              onClick={() => setShowAdvancedOptions(!showAdvancedOptions)}
              className={cn(
                "absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-lg transition-all",
                showAdvancedOptions
                  ? "text-accent-400 bg-accent-500/20"
                  : "text-white/60 hover:text-accent-400 hover:bg-accent-500/20"
              )}
            >
              {showAdvancedOptions ? <X size={18} /> : <Sparkles size={18} />}
            </button>
          )}
        </div>

        {/* Advanced Options */}
        <div
          className={cn(
            "overflow-hidden transition-all duration-300 ease-in-out",
            showAdvancedOptions ? "max-h-[500px] opacity-100" : "max-h-0 opacity-0"
          )}
        >
          <div className="space-y-4 pt-3">
            {/* Description Field */}
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add details (optional)..."
              rows={2}
              className="w-full px-4 py-3 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all resize-none text-white placeholder:text-white/40"
              disabled={isPending}
            />

            {/* Priority */}
            <div>
              <label className="block text-sm font-medium text-white/70 mb-1">
                Priority
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="w-full px-4 py-3 rounded-xl backdrop-blur-xl bg-slate-900/70 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all text-white"
              >
                <option value="low" className="bg-slate-900 text-white">Low</option>
                <option value="medium" className="bg-slate-900 text-white">Medium</option>
                <option value="high" className="bg-slate-900 text-white">High</option>
              </select>
            </div>

            {/* Due Date */}
            <div>
              <label className="block text-sm font-medium text-white/70 mb-1">
                Due Date (optional)
              </label>
              <div className="relative">
                <input
                  type="datetime-local"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  className="w-full px-4 py-3 pl-10 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all text-white"
                />
                <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/60" size={18} />
              </div>
            </div>

            {/* Recurrence Pattern */}
            <div>
              <label className="block text-sm font-medium text-white/70 mb-1">
                Recurrence Pattern (optional)
              </label>
              <div className="relative">
                <select
                  value={recurrencePattern}
                  onChange={(e) => setRecurrencePattern(e.target.value)}
                  className="w-full px-4 py-3 pl-10 rounded-xl backdrop-blur-xl bg-slate-900/70 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all text-white"
                >
                  <option value="" className="bg-slate-900 text-white">None</option>
                  <option value="daily" className="bg-slate-900 text-white">Daily</option>
                  <option value="weekly" className="bg-slate-900 text-white">Weekly</option>
                  <option value="monthly" className="bg-slate-900 text-white">Monthly</option>
                </select>
                <Repeat className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/60" size={18} />
              </div>
            </div>

            {/* Tags */}
            <div>
              <label className="block text-sm font-medium text-white/70 mb-1">
                Tags (comma separated, optional)
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                  placeholder="work, personal, urgent"
                  className="w-full px-4 py-3 pl-10 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all text-white placeholder:text-white/40"
                />
                <Tag className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/60" size={18} />
              </div>
            </div>
          </div>
        </div>
      </div>

      <button
        type="submit"
        disabled={isPending || !title.trim()}
        className="w-full group relative px-6 py-3.5 rounded-xl font-semibold text-white transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
      >
        {/* Gradient Background */}
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-accent-500 transition-transform duration-300 group-hover:scale-105"></div>

        {/* Glow Effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-accent-400 blur-xl opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>

        {/* Content */}
        <span className="relative flex items-center justify-center gap-2">
          {isPending ? (
            <>
              <Loader2 size={20} className="animate-spin" />
              <span>Adding...</span>
            </>
          ) : (
            <>
              <Plus size={20} strokeWidth={2.5} />
              <span>Add Task</span>
            </>
          )}
        </span>
      </button>
    </form>
  );
}
