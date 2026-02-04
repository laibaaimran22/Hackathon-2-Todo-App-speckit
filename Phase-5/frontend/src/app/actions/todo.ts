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

export async function addTodo(
    title: string,
    description?: string,
    priority?: string,
    due_date?: string,
    recurrence_pattern?: string,
    tag_names?: string[]
) {
    const authHeaders = await getAuthHeader();

    const body: Record<string, any> = { title };
    if (description) body.description = description;
    if (priority) body.priority = priority;
    if (due_date) body.due_date = due_date;
    if (recurrence_pattern) body.recurrence_pattern = recurrence_pattern;
    if (tag_names) body.tag_names = tag_names;

    try {
        const response = await apiClient("/api/tasks", {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                ...authHeaders,
                "Content-Type": "application/json"
            }
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

export async function updateTodo(
    id: number,
    title: string,
    description?: string,
    priority?: string,
    due_date?: string,
    recurrence_pattern?: string,
    tag_names?: string[]
) {
    const authHeaders = await getAuthHeader();

    const body: Record<string, any> = { title };
    if (description !== undefined) body.description = description;
    if (priority !== undefined) body.priority = priority;
    if (due_date !== undefined) body.due_date = due_date;
    if (recurrence_pattern !== undefined) body.recurrence_pattern = recurrence_pattern;
    if (tag_names !== undefined) body.tag_names = tag_names;

    try {
        const response = await apiClient(`/api/tasks/${id}`, {
            method: "PUT",
            body: JSON.stringify(body),
            headers: {
                ...authHeaders,
                "Content-Type": "application/json"
            }
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
