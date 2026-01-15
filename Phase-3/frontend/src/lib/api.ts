const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // This function is kept for general API calls
  // For authenticated calls, use server actions that have access to JWT tokens
  // Better Auth client session may not directly expose JWT tokens

  const headers = new Headers(options.headers);
  headers.set('Content-Type', 'application/json');

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'An unknown error occurred' }));
    throw new Error(error.message || `HTTP error! status: ${response.status}`);
  }

  if (response.status === 204) return null;
  return response.json();
}
