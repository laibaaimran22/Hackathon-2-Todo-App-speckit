"use server";

import { apiClient } from "@/lib/api-client";
import { revalidatePath } from "next/cache";
import { getJwtToken } from "@/lib/auth-utils";

async function getAuthHeader() {
    // Get the JWT token instead of the session token
    const token = await getJwtToken();

    if (!token) {
        throw new Error("Unauthorized - no token available");
    }

    return {
        "Authorization": `Bearer ${token}`
    };
}

export async function addTodo(formData: FormData) {
    const title = formData.get("title") as string;
    const description = formData.get("description") as string | null;
    const authHeaders = await getAuthHeader();

    const body: Record<string, string> = { title };
    if (description) {
        body.description = description;
    }

    await apiClient("/api/tasks", {
        method: "POST",
        body: JSON.stringify(body),
        headers: authHeaders
    });

    revalidatePath("/dashboard");
}

export async function toggleTodo(id: string, is_completed: boolean) {
    const authHeaders = await getAuthHeader();

    await apiClient(`/api/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify({ is_completed }),
        headers: authHeaders
    });

    revalidatePath("/dashboard");
}

export async function deleteTodo(id: string) {
    const authHeaders = await getAuthHeader();

    await apiClient(`/api/tasks/${id}`, {
        method: "DELETE",
        headers: authHeaders
    });

    revalidatePath("/dashboard");
}

export async function updateTodo(id: string, title: string, description?: string) {
    const authHeaders = await getAuthHeader();

    const body: Record<string, string> = { title };
    if (description !== undefined) {
        body.description = description;
    }

    await apiClient(`/api/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify(body),
        headers: authHeaders
    });

    revalidatePath("/dashboard");
}
