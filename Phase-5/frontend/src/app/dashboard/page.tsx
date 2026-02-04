import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { Todo } from "@/types";
import { DashboardClient } from "./DashboardClient";

async function getTodos(token: string): Promise<Todo[]> {
  try {
    console.log("[Dashboard] Fetching todos with token from:", process.env.NEXT_PUBLIC_API_URL);
    // Direct server-side API call with the token
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      cache: 'no-store' // Disable caching for fresh data
    });

    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Unknown error');
      console.error(`[Dashboard] Failed to fetch todos: ${response.status} ${response.statusText}`, errorText);
      // Return an empty array if there's an error, but log the error
      return [];
    }

    const data = await response.json();
    console.log("[Dashboard] Successfully fetched todos:", data.length);
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("[Dashboard] Failed to fetch todos:", error);
    // Return empty array in case of error to prevent server component crashes
    return [];
  }
}

async function getUserInfoAndToken() {
  // Get the auth token from cookies
  const cookieStore = await cookies();
  const token = cookieStore.get('auth-token')?.value;

  if (!token) {
    console.log("[Dashboard] No auth token found in cookies");
    return { userInfo: null, token: "" };
  }

  try {
    console.log("[Dashboard] Verifying token with backend");
    // Verify the token by making a request to the backend
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/user`, {
      headers: { "Authorization": `Bearer ${token}` },
      cache: 'no-store'
    });

    if (!response.ok) {
      console.error(`[Dashboard] Token verification failed: ${response.status}`);
      return { userInfo: null, token: "" };
    }

    const userData = await response.json();
    console.log("[Dashboard] Token verified successfully");

    // Extract a more user-friendly name from the user data
    // Prioritize the actual email over user ID
    let displayName = "User";
    if (userData.email && !userData.email.includes('@example.com')) {
      // If it's a real email (not the placeholder), use the part before @ as display name
      displayName = userData.email.split('@')[0];
    } else if (userData.email && userData.email.includes('@example.com')) {
      // If it's the default email format with user ID, try to get a friendlier name
      const userId = userData.id || userData.sub || userData.user_id;
      if (userId && userId.startsWith('user_')) {
        // Use the part after 'user_' as a display name, or just show "User"
        const suffix = userId.substring(5); // Remove 'user_' prefix
        displayName = `User ${suffix.substring(0, 8)}`; // Show first 8 chars
      }
    } else if (userData.name) {
      displayName = userData.name;
    } else if (userData.username) {
      displayName = userData.username;
    }

    return {
      userInfo: {
        ...userData,
        displayName
      },
      token
    };
  } catch (error) {
    console.error("[Dashboard] Failed to verify token:", error);
    return { userInfo: null, token: "" };
  }
}

export default async function DashboardPage() {
  const { userInfo, token } = await getUserInfoAndToken();

  if (!token) {
    redirect("/login");
  }

  const userEmail = userInfo?.displayName || userInfo?.email || userInfo?.user?.email || "User";
  const todos = token ? await getTodos(token) : [];

  return (
    <DashboardClient
      userEmail={userEmail}
      todos={todos}
    />
  );
}