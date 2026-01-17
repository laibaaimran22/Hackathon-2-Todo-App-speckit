const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // Retrieve auth token by calling the token endpoint
  let token = null;
  try {
    const tokenResponse = await fetch('/api/token');
    if (tokenResponse.ok) {
      const tokenData = await tokenResponse.json();
      token = tokenData.token;
    }
  } catch (error) {
    console.error('Failed to retrieve token:', error);
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
