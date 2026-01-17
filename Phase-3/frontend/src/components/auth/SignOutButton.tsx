"use client";

import { useRouter } from "next/navigation";
import { LogOut, Loader2 } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

export function SignOutButton() {
    const router = useRouter();
    const [isPending, setIsPending] = useState(false);

    const handleSignOut = async () => {
        if (isPending) return; // Prevent double click

        setIsPending(true);

        try {
            // Directly call backend signout endpoint
            await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/sign-out`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            // Clear the stored token from localStorage and cookie
            if (typeof window !== 'undefined') {
                localStorage.removeItem('auth-token');
                // Clear the auth cookie
                document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
            }

            // Show success toast
            toast.success("Signed out successfully!", {
                description: "See you again soon!",
            });
        } catch (error) {
            console.error("Sign out error:", error);
            // Clear the stored token from localStorage even if backend call fails
            if (typeof window !== 'undefined') {
                localStorage.removeItem('auth-token');
            }

            // Show toast even on error since we'll sign out anyway
            toast.info("Signed out", {
                description: "You've been signed out.",
            });
        } finally {
            // Small delay to ensure state is properly cleared before redirect
            setTimeout(() => {
              router.push("/");
            }, 100);
        }
    };

    return (
        <button
            onClick={handleSignOut}
            disabled={isPending}
            className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-white/80 hover:text-white hover:bg-white/10 rounded-xl transition-all duration-200 border border-white/20 hover:border-white/30 backdrop-blur-xl disabled:opacity-50 disabled:cursor-not-allowed"
        >
            {isPending ? (
                <Loader2 size={18} className="animate-spin" />
            ) : (
                <LogOut size={18} />
            )}
            <span className="hidden sm:inline">{isPending ? "Signing out..." : "Sign Out"}</span>
        </button>
    );
}
