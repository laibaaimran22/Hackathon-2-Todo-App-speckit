import { NextRequest } from 'next/server';
import { cookies } from 'next/headers';

export async function GET(request: NextRequest) {
  try {
    // Get the auth token from cookies that was stored during login
    const cookieStore = await cookies();
    const token = cookieStore.get('auth-token')?.value;

    if (!token) {
      return Response.json({ error: 'No active session' }, { status: 401 });
    }

    // Return the token that's stored in cookies
    return Response.json({ token });
  } catch (error) {
    console.error('Error getting token:', error);
    return Response.json({ error: 'Failed to get token' }, { status: 500 });
  }
}