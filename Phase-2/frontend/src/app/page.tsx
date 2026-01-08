"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import {
  CheckCircle2,
  Shield,
  Zap,
  Users,
  ArrowRight,
  Sparkles,
  Play
} from "lucide-react";

export default function Home() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [activeFeature, setActiveFeature] = useState(0);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const features = [
    {
      icon: Shield,
      title: "Secure Authentication",
      description: "Powered by Better Auth with JWT tokens for enterprise-grade security",
      color: "from-emerald-500 to-teal-600"
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Built with Next.js 15 and FastAPI for blazing performance",
      color: "from-amber-500 to-orange-600"
    },
    {
      icon: Users,
      title: "User Isolation",
      description: "Your tasks are private - only you can access your data",
      color: "from-violet-500 to-purple-600"
    }
  ];

  const stats = [
    { value: "5", label: "Core Features" },
    { value: "100%", label: "Secure" },
    { value: "0", label: "Delay" },
    { value: "∞", label: "Tasks" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-brand-teal-950 to-slate-900 overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-brand-teal-500/20 to-transparent rounded-full blur-3xl animate-pulse" />
        <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-brand-coral-500/20 to-transparent rounded-full blur-3xl animate-pulse" style={{ animationDelay: "1s" }} />
      </div>

      {/* Navigation */}
      <nav className={`relative z-10 transition-all duration-700 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-4"}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-teal-500 to-brand-coral-500 flex items-center justify-center shadow-lg shadow-brand-teal-500/25">
                <CheckCircle2 className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Todo Evolution</span>
            </div>
            <div className="flex items-center gap-4">
              <Link
                href="/login"
                className="px-5 py-2.5 text-white/80 hover:text-white font-medium transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/signup"
                className="px-5 py-2.5 bg-white/10 hover:bg-white/20 text-white font-medium rounded-xl border border-white/20 backdrop-blur-sm transition-all"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10">
        <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-32 transition-all duration-700 delay-100 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
          {/* Badge */}
          <div className="flex justify-center mb-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-white/80">Phase 2 - Spec-Driven Development</span>
            </div>
          </div>

          {/* Main Heading */}
          <div className="text-center max-w-4xl mx-auto">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
              Manage Tasks
              <span className="block bg-gradient-to-r from-brand-teal-400 via-brand-amber-400 to-brand-coral-400 bg-clip-text text-transparent">
                Evolved
              </span>
            </h1>
            <p className="text-xl text-white/60 max-w-2xl mx-auto mb-10">
              A modern, secure, and beautiful task management application built with
              Next.js 15, FastAPI, and Better Auth. Your tasks, evolutionized.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Link
                href="/signup"
                className="group inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-brand-teal-500 to-brand-coral-500 text-white font-semibold rounded-2xl shadow-lg shadow-brand-teal-500/25 hover:shadow-brand-teal-500/40 transition-all duration-300 hover:scale-105"
              >
                Get Started Free
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/login"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 text-white/80 hover:text-white font-medium rounded-2xl border border-white/20 hover:bg-white/10 transition-all duration-300"
              >
                <Play className="w-5 h-5" />
                Sign In
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
              {stats.map((stat) => (
                <div
                  key={stat.label}
                  className="p-4 rounded-2xl bg-white/5 backdrop-blur-sm border border-white/10 text-center"
                >
                  <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                  <div className="text-sm text-white/50">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-700 delay-300 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
          <div className="grid md:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div
                key={`${feature.title}-${index}`}
                onMouseEnter={() => setActiveFeature(index)}
                className={`group p-8 rounded-3xl bg-white/5 backdrop-blur-sm border transition-all duration-300 cursor-pointer ${
                  activeFeature === index
                    ? "bg-white/10 border-white/20 scale-105"
                    : "border-white/10 hover:bg-white/10"
                }`}
              >
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                <p className="text-white/60">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Tech Stack */}
        <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 transition-all duration-700 delay-500 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}>
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">Built with Modern Tech</h2>
            <p className="text-white/60">Best-in-class technologies for the best experience</p>
          </div>
          <div className="flex flex-wrap justify-center gap-4">
            {["Next.js 15", "FastAPI", "PostgreSQL", "Better Auth", "Tailwind CSS", "TypeScript"].map((tech) => (
              <span
                key={tech}
                className="px-6 py-3 rounded-full bg-white/5 border border-white/10 text-white/80 font-medium hover:bg-white/10 transition-colors"
              >
                {tech}
              </span>
            ))}
          </div>
        </div>

        {/* Footer */}
        <footer className="border-t border-white/10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-teal-500 to-brand-coral-500 flex items-center justify-center">
                  <CheckCircle2 className="w-5 h-5 text-white" />
                </div>
                <span className="text-white/60 text-sm">Todo Evolution Phase 2</span>
              </div>
              <p className="text-white/40 text-sm">
                Spec-Driven Development Hackathon Project
              </p>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
