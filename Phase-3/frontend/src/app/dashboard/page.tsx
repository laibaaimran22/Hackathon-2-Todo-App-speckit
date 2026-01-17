import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { apiClient } from "@/lib/api-client";
import { Todo } from "@/types";
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

async function getUserInfoAndToken() {
  // Get the auth token from cookies
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;

  if (!token) {
    return { userInfo: null, token: "" };
  }

  try {
    // Verify the token by making a request to the backend
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/user`, {
      headers: { "Authorization": `Bearer ${token}` },
      cache: 'no-store'
    });

    if (!response.ok) {
      return { userInfo: null, token: "" };
    }

    const userData = await response.json();
    return { userInfo: userData, token };
  } catch (error) {
    console.error("Failed to verify token:", error);
    return { userInfo: null, token: "" };
  }
}

export default async function DashboardPage() {
  const { userInfo, token } = await getUserInfoAndToken();

  if (!token) {
    redirect("/login");
  }

  const userEmail = userInfo?.email || userInfo?.user?.email || "User";
  const todos = token ? await getTodos(token) : [];

  return (
    <DashboardClient
      userEmail={userEmail}
      todos={todos}
    />
  );
}