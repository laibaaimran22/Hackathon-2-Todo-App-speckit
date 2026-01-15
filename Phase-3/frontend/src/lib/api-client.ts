/**
 * API Client Fetch Wrapper
 * Handles base URL, default headers, and common error scenarios.
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;

  // Merge headers properly - Authorization header should be preserved
  const headers = new Headers({
    "Content-Type": "application/json",
  });

  // If options.headers exists, add them to our headers object
  if (options.headers) {
    const existingHeaders = options.headers;
    if (existingHeaders instanceof Headers) {
      for (const [key, value] of existingHeaders.entries()) {
        headers.set(key, value);
      }
    } else if (Array.isArray(existingHeaders)) {
      for (const [key, value] of existingHeaders) {
        headers.set(key, value);
      }
    } else {
      // Handle plain object
      const headerObj = existingHeaders as Record<string, string>;
      for (const [key, value] of Object.entries(headerObj)) {
        headers.set(key, value);
      }
    }
  }

  // Create a copy of options without headers to avoid conflict
  const optionsWithoutHeaders = { ...options };
  delete optionsWithoutHeaders.headers;

  const response = await fetch(url, {
    ...optionsWithoutHeaders,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
