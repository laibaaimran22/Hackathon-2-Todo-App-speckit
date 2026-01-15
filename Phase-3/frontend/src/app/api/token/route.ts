import { NextRequest } from 'next/server';
import { getJwtToken } from '@/lib/auth-utils';
import { auth } from '@/lib/auth';

export async function GET(request: NextRequest) {
  try {
    // Get the session using Better Auth
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session || !session.session) {
      return Response.json({ error: 'No active session' }, { status: 401 });
    }

    // Generate JWT token using the server-side utility
    const token = await getJwtToken();

    return Response.json({ token });
  } catch (error) {
    console.error('Error getting token:', error);
    return Response.json({ error: 'Failed to get token' }, { status: 500 });
  }
}