export const dynamic = "force-dynamic";
export const revalidate = 0;
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { getJwtToken } from "@/lib/auth-utils";
import { DashboardClient } from "./DashboardClient";

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
    <DashboardClient
      userEmail={session.user.email}
      jwtToken={jwtToken}
    />
  );
}