"use client";

import { useState } from "react";
import { Plus, Loader2, Sparkles, X } from "lucide-react";
import { addTodo } from "@/app/actions/todo";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function AddTodoForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isPending, setIsPending] = useState(false);
  const [showDescription, setShowDescription] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setIsPending(true);
    try {
      const formData = new FormData();
      formData.append("title", title.trim());
      if (description.trim()) {
        formData.append("description", description.trim());
      }
      await addTodo(formData);
      setTitle("");
      setDescription("");
      setShowDescription(false);
    } catch (error) {
      console.error("Failed to add todo:", error);
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
              if (e.target.value.trim() && !showDescription) {
                setShowDescription(true);
              }
            }}
            placeholder="What needs to be done?"
            className="w-full px-4 py-3.5 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all text-white placeholder:text-white/40 text-base"
            disabled={isPending}
          />
          {title.trim() && (
            <button
              type="button"
              onClick={() => setShowDescription(!showDescription)}
              className={cn(
                "absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-lg transition-all",
                showDescription
                  ? "text-accent-400 bg-accent-500/20"
                  : "text-white/60 hover:text-accent-400 hover:bg-accent-500/20"
              )}
            >
              {showDescription ? <X size={18} /> : <Sparkles size={18} />}
            </button>
          )}
        </div>

        {/* Description Field */}
        <div
          className={cn(
            "overflow-hidden transition-all duration-300 ease-in-out",
            showDescription ? "max-h-40 opacity-100" : "max-h-0 opacity-0"
          )}
        >
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add details (optional)..."
            rows={2}
            className="w-full px-4 py-3 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all resize-none text-white placeholder:text-white/40"
            disabled={isPending}
          />
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
