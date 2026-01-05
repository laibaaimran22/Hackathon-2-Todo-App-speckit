"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import { Sparkles, Mail, Lock, ArrowRight, Loader2 } from "lucide-react";
import { toast } from "sonner";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    if (loading) return; // Prevent double submission

    setLoading(true);
    setError("");

    try {
      const result = await authClient.signIn.email({
        email,
        password,
      });

      if (result.data) {
        // Success - show toast and redirect
        toast.success("Successfully signed in!", {
          description: "Welcome back! Redirecting to dashboard...",
        });

        // Use replace for faster navigation (no history entry)
        router.replace("/dashboard");
      } else if (result.error) {
        const errorMsg = result.error.message || "Invalid credentials";
        setError(errorMsg);
        toast.error("Sign in failed", {
          description: errorMsg,
        });
        setLoading(false);
      }
    } catch (err: any) {
      console.error("Login error:", err);
      const errorMsg = "An unexpected error occurred. Please try again.";
      setError(errorMsg);
      toast.error("Sign in failed", {
        description: errorMsg,
      });
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-primary-900 to-slate-950 relative overflow-hidden flex items-center justify-center p-4">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-accent-500/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Content */}
      <div className="relative z-10 w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 mb-4 animate-glow">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-white/60">Sign in to continue your productivity journey</p>
        </div>

        {/* Form Card */}
        <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl p-8 shadow-2xl">
          {error && (
            <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-5">
            {/* Email Field */}
            <div>
              <label className="block text-sm font-semibold text-white/80 mb-2">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">
                  <Mail size={18} />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full pl-12 pr-4 py-3.5 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all text-white placeholder:text-white/40"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-semibold text-white/80 mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">
                  <Lock size={18} />
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-12 pr-4 py-3.5 rounded-xl backdrop-blur-xl bg-white/10 border border-white/20 focus:border-primary-400 focus:ring-2 focus:ring-primary-500/50 outline-none transition-all text-white placeholder:text-white/40"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full group relative px-6 py-3.5 rounded-xl font-semibold text-white transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden mt-6"
            >
              {/* Gradient Background */}
              <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-accent-500 transition-transform duration-300 group-hover:scale-105"></div>

              {/* Glow Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-accent-400 blur-xl opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>

              {/* Content */}
              <span className="relative flex items-center justify-center gap-2">
                {loading ? (
                  <>
                    <Loader2 size={20} className="animate-spin" />
                    <span>Signing in...</span>
                  </>
                ) : (
                  <>
                    <span>Sign In</span>
                    <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </span>
            </button>
          </form>

          {/* Sign Up Link */}
          <div className="mt-8 pt-6 border-t border-white/10 text-center">
            <p className="text-white/60 text-sm">
              Don't have an account?{" "}
              <Link
                href="/signup"
                className="text-primary-400 hover:text-primary-300 font-semibold transition-colors"
              >
                Sign Up
              </Link>
            </p>
          </div>
        </div>

        {/* Features */}
        <div className="mt-8 grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-white mb-1">✨</div>
            <div className="text-xs text-white/60">Modern UI</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-white mb-1">🔒</div>
            <div className="text-xs text-white/60">Secure</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-white mb-1">⚡</div>
            <div className="text-xs text-white/60">Fast</div>
          </div>
        </div>
      </div>
    </div>
  );
}
