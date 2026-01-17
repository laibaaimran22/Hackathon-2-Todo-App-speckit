/**
 * API Client Fetch Wrapper
 * Handles base URL, default headers, and common error scenarios.
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Retrieve auth token from localStorage
  let token = null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('auth-token');
  }

  const url = `${BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;

  // Merge headers properly - Authorization header should be preserved
  const headers = new Headers({
    "Content-Type": "application/json",
  });

  // Add authorization header if token exists
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

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

  // If we get a 401 or 403, clear the token as it might be invalid/expired
  if (response.status === 401 || response.status === 403) {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth-token');
      document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
