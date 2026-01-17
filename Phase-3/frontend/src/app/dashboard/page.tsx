import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { apiClient } from "@/lib/api-client";
import { Todo } from "@/types";
import { getJwtToken } from "@/lib/auth-utils";
import { DashboardClient } from "./DashboardClient";

async function getTodos(token: string): Promise<Todo[]> {
  try {
    const data = await apiClient<Todo[]>("/api/tasks", {
      headers: { "Authorization": `Bearer ${token}` },
      next: { revalidate: 0 }
    });
    return data;
  } catch (error) {
    console.error("Failed to fetch todos:", error);
    return [];
  }
}

async function getSessionAndToken() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session?.session) {
    return { session: null, token: "" };
  }

  const token = await getJwtToken();
  return { session, token };
}

export default async function DashboardPage() {
  const { session, token } = await getSessionAndToken();

  if (!session?.session) {
    redirect("/login");
  }

  const userEmail = session?.user?.email || "User";
  const todos = token ? await getTodos(token) : [];

  return (
    <DashboardClient
      userEmail={userEmail}
      todos={todos}
    />
  );
}