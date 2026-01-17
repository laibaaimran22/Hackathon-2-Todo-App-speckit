import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Since we're storing the token in localStorage and not using Better Auth session,
    // we'll return a message indicating this approach
    // In a real implementation, you might want to implement a server-side session mechanism
    // that can validate the token and return it

    return Response.json({
      error: 'Direct token retrieval not available with this approach. Token is stored in browser localStorage.'
    }, { status: 404 });
  } catch (error) {
    console.error('Error getting token:', error);
    return Response.json({ error: 'Failed to get token' }, { status: 500 });
  }
}