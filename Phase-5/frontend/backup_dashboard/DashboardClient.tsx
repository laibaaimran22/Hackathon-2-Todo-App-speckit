'use client';

import { Suspense } from 'react';
import { TodoSkeleton } from '@/components/ui/Skeleton';
import { ClientTodoSection } from '@/components/todo/ClientTodoSection';
import { ClientAddTodoForm } from '@/components/todo/ClientAddTodoForm';
import { ClientSignOutButton } from '@/components/auth/ClientSignOutButton';

interface DashboardClientProps {
  userEmail: string;
  jwtToken: string;
}

export function DashboardClient({ userEmail, jwtToken }: DashboardClientProps) {
  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8">
      <header className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-3xl font-bold text-brand-slate">My Dashboard</h1>
          <p className="text-gray-500">Welcome back, {userEmail}</p>
        </div>
        <ClientSignOutButton />
      </header>

      <main className="space-y-8">
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h2 className="text-xl font-semibold mb-4 text-brand-slate">Add New Task</h2>
          <ClientAddTodoForm />
        </section>

        <section>
          <Suspense fallback={<TodoSkeleton />}>
            <ClientTodoSection token={jwtToken} />
          </Suspense>
        </section>
      </main>
    </div>
  );
}