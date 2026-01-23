const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // Retrieve auth token from localStorage
  let token: string | null = null;
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('auth-token');
  }

  const headers = new Headers(options.headers);
  headers.set('Content-Type', 'application/json');

  // Add authorization header if token exists and is valid
  if (token && token !== 'null' && token !== 'undefined' && token.trim() !== '') {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
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
    const error = await response.json().catch(() => ({ message: 'An unknown error occurred' }));
    throw new Error(error.message || `HTTP error! status: ${response.status}`);
  }

  if (response.status === 204) return null;
  return response.json();
}
