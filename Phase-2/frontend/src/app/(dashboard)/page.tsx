export const dynamic = "force-dynamic";
export const revalidate = 0;
import { Suspense } from "react";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { apiClient } from "@/lib/api-client";
import { Todo } from "@/types";
import { ClientTodoSection } from "@/components/todo/ClientTodoSection";
import { ClientAddTodoForm } from "@/components/todo/ClientAddTodoForm";
import { ClientSignOutButton } from "@/components/auth/ClientSignOutButton";
import { TodoSkeleton } from "@/components/ui/Skeleton";
import { getJwtToken } from "@/lib/auth-utils";


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