import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
    // Ensure the basePath matches the server configuration
    basePath: "/api/auth",
});
