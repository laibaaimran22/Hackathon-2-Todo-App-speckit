const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // Retrieve auth token from localStorage
  let token = null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('auth-token');
  }

  const headers = new Headers(options.headers);
  headers.set('Content-Type', 'application/json');

  // Add authorization header if token exists
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

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
