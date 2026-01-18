/**
 * API Client Fetch Wrapper
 * Handles base URL, default headers, and common error scenarios.
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {},
  tokenOverride?: string | null // Allow token to be passed explicitly for server-side calls
): Promise<T> {
  // Retrieve auth token from localStorage if not overridden
  let token: string | undefined | null = tokenOverride;
  if (!token && typeof window !== 'undefined') {
    token = localStorage.getItem('auth-token');
  }

  const url = `${BASE_URL}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;

  // Merge headers properly - Authorization header should be preserved
  const headers = new Headers({
    "Content-Type": "application/json",
  });

  // Add authorization header if token exists and is valid
  if (token && token !== 'null' && token !== 'undefined' && token.trim() !== '') {
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
    if (typeof window !== 'undefined' && !tokenOverride) { // Only clear if not using override
      localStorage.removeItem('auth-token');
      document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
  }

  if (!response.ok) {
    try {
      const errorData = await response.json();
      console.error(`[API Error] ${response.status} - ${url}:`, errorData);
      throw new Error(errorData.detail || errorData.message || `API Error: ${response.status} ${response.statusText}`);
    } catch (e) {
      if (e instanceof Error && e.message.includes('API Error')) {
        throw e;
      }
      console.error(`[API Error] ${response.status} - ${url}: Failed to parse error response`);
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }
  }

  return response.json();
}
