"use server";

import { apiClient } from "@/lib/api-client";
import { revalidatePath } from "next/cache";
import { getJwtToken } from "@/lib/auth-utils";

async function getAuthHeader() {
    try {
        // Get the JWT token instead of the session token
        const token = await getJwtToken();

        if (!token) {
            throw new Error("Unauthorized - no token available");
        }

        return {
            "Authorization": `Bearer ${token}`
        };
    } catch (error) {
        console.error("Error getting auth header:", error);
        throw new Error(`Authentication failed: ${(error as Error).message}`);
    }
}

export async function addTodo(formData: FormData) {
    const title = formData.get("title") as string;
    const description = formData.get("description") as string | null;
    const authHeaders = await getAuthHeader();

    const body: Record<string, string> = { title };
    if (description) {
        body.description = description;
    }

    try {
        const response = await apiClient("/api/tasks", {
            method: "POST",
            body: JSON.stringify(body),
            headers: authHeaders
        });

        revalidatePath("/dashboard");
        revalidatePath("/"); // Also revalidate home page if needed

        return response;
    } catch (error) {
        // Revalidate to ensure UI is in sync and re-throw
        revalidatePath("/dashboard");
        revalidatePath("/");
        throw error;
    }
}

export async function toggleTodo(id: number, is_completed: boolean) {
    const authHeaders = await getAuthHeader();

    try {
        const response = await apiClient(`/api/tasks/${id}/complete`, {
            method: "PATCH",
            headers: authHeaders
        });

        revalidatePath("/dashboard");
        revalidatePath("/"); // Also revalidate home page if needed

        return response;
    } catch (error) {
        // Revalidate to ensure UI is in sync and re-throw
        revalidatePath("/dashboard");
        revalidatePath("/");
        throw error;
    }
}

export async function deleteTodo(id: number) {
    const authHeaders = await getAuthHeader();

    try {
        const response = await apiClient(`/api/tasks/${id}`, {
            method: "DELETE",
            headers: authHeaders
        });

        revalidatePath("/dashboard");
        revalidatePath("/"); // Also revalidate home page if needed

        return response;
    } catch (error) {
        // If the task doesn't exist, it might have already been deleted
        // Just revalidate to ensure UI is in sync and return success
        if (error instanceof Error && error.message.includes("Task not found")) {
            revalidatePath("/dashboard");
            revalidatePath("/");
            return { status: "success", message: "Task was already deleted" };
        }
        // For other errors, revalidate and re-throw
        revalidatePath("/dashboard");
        revalidatePath("/");
        throw error;
    }
}

export async function updateTodo(id: number, title: string, description?: string) {
    const authHeaders = await getAuthHeader();

    const body: Record<string, string> = { title };
    if (description !== undefined) {
        body.description = description;
    }

    try {
        const response = await apiClient(`/api/tasks/${id}`, {
            method: "PUT",
            body: JSON.stringify(body),
            headers: authHeaders
        });

        revalidatePath("/dashboard");
        revalidatePath("/"); // Also revalidate home page if needed

        return response;
    } catch (error) {
        // Revalidate to ensure UI is in sync and re-throw
        revalidatePath("/dashboard");
        revalidatePath("/");
        throw error;
    }
}
