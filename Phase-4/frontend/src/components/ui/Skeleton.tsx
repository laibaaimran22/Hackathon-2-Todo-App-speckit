"use client";

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-gray-200", className)}
      {...props}
    />
  );
}

export function TodoSkeleton() {
    return (
        <div className="space-y-3">
            {[1, 2, 3].map((i) => (
                <div key={i} className="p-4 bg-white rounded-xl border border-gray-100 flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1">
                        <Skeleton className="h-6 w-6 rounded-full" />
                        <Skeleton className="h-6 w-1/3" />
                    </div>
                </div>
            ))}
        </div>
    );
}
