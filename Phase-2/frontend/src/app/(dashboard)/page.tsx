export const dynamic = "force-dynamic";
export const revalidate = 0;
import { Suspense } from "react";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { apiClient } from "@/lib/api-client";
import { Todo } from "@/types";
import { TodoList } from "@/components/todo/TodoList";
import { AddTodoForm } from "@/components/todo/AddTodoForm";
import { SignOutButton } from "@/components/auth/SignOutButton";
import { TodoSkeleton } from "@/components/ui/Skeleton";
import { getJwtToken } from "@/lib/auth-utils";

async function TodoDataSection({ token }: { token: string }) {
  let todos: Todo[] = [];
  try {
    todos = await apiClient<Todo[]>("/api/tasks", {
      headers: {
        "Authorization": `Bearer ${token}`
      },
      next: { revalidate: 0 }
    });
  } catch (error) {
    console.error("Failed to fetch todos:", error);
    return <div className="p-4 text-red-500 bg-red-50 rounded-lg">Failed to load tasks. Please try again.</div>;
  }

  return (
    <>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-brand-slate">Your Tasks</h2>
        <span className="bg-brand-indigo/10 text-brand-indigo text-xs font-bold px-2 py-1 rounded-full">
          {todos.length} Total
        </span>
      </div>
      <TodoList initialTodos={todos} />
    </>
  );
}

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session || !session.session) {
    redirect("/login");
  }

  // Get the JWT token instead of the session token
  let jwtToken: string;
  try {
    jwtToken = await getJwtToken();
  } catch (error) {
    console.error("Failed to get JWT token:", error);
    redirect("/login"); // Redirect to login if JWT token cannot be obtained
  }

  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8">
      <header className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-3xl font-bold text-brand-slate">My Dashboard</h1>
          <p className="text-gray-500">Welcome back, {session.user.email}</p>
        </div>
        <SignOutButton />
      </header>

      <main className="space-y-8">
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h2 className="text-xl font-semibold mb-4 text-brand-slate">Add New Task</h2>
          <AddTodoForm />
        </section>

        <section>
          <Suspense fallback={
            <>
              <h2 className="text-xl font-semibold mb-4 text-brand-slate">Your Tasks</h2>
              <TodoSkeleton />
            </>
          }>
            <TodoDataSection token={jwtToken} />
          </Suspense>
        </section>
      </main>
    </div>
  );
}