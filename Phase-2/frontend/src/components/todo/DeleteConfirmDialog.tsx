"use client";

import { useState } from "react";
import { AlertTriangle, X, Trash2, Loader2 } from "lucide-react";

interface DeleteConfirmDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => Promise<void>;
  taskTitle: string;
}

export function DeleteConfirmDialog({
  isOpen,
  onClose,
  onConfirm,
  taskTitle,
}: DeleteConfirmDialogProps) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleConfirm = async () => {
    setIsDeleting(true);
    try {
      await onConfirm();
      onClose();
    } finally {
      setIsDeleting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm animate-fade-in"
        onClick={onClose}
      />

      {/* Dialog */}
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 animate-scale-in">
        {/* Icon */}
        <div className="flex justify-center pt-8">
          <div className="p-4 bg-red-100 rounded-full">
            <AlertTriangle size={32} className="text-red-600" />
          </div>
        </div>

        {/* Content */}
        <div className="p-6 text-center">
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Delete Task?</h3>
          <p className="text-gray-500 mb-2">
            Are you sure you want to delete
          </p>
          <p className="text-gray-800 font-medium truncate px-4">
            &ldquo;{taskTitle}&rdquo;
          </p>
          <p className="text-gray-400 text-sm mt-2">
            This action cannot be undone.
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-3 px-6 pb-6">
          <button
            onClick={onClose}
            disabled={isDeleting}
            className="flex-1 px-4 py-3 text-gray-700 font-medium bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleConfirm}
            disabled={isDeleting}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-3 text-white font-medium bg-red-600 hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl transition-colors"
          >
            {isDeleting ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Deleting...
              </>
            ) : (
              <>
                <Trash2 size={18} />
                Delete
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
