'use server';

import { auth } from '@/lib/auth';
import { cookies } from 'next/headers';
import * as jose from 'jose';

/**
 * Generate a JWT token for the authenticated user.
 * Better Auth manages sessions, but we need to create our own JWT
 * for the FastAPI backend to verify.
 *
 * Flow:
 * 1. Get session from Better Auth (validates user is authenticated)
 * 2. Extract user ID from session
 * 3. Create JWT with user ID using shared JWT_SECRET
 * 4. Backend verifies JWT and extracts user ID
 */
export async function getJwtToken(): Promise<string> {
  try {
    // Get cookies for Better Auth session
    const cookieStore = await cookies();
    const allCookies = cookieStore.getAll();
    const cookieHeader = allCookies.map(c => `${c.name}=${c.value}`).join('; ');

    // Get the current session from Better Auth
    const session = await auth.api.getSession({
      headers: new Headers({
        'cookie': cookieHeader
      })
    });

    if (!session || !session.session) {
      throw new Error('No active session');
    }

    // Get user info from session
    const userId = session.user.id;
    const email = session.user.email;

    // Create JWT for the backend
    const secret = new TextEncoder().encode(
      process.env.JWT_SECRET || process.env.BETTER_AUTH_SECRET || 'development-secret-key'
    );

    // Generate JWT with user ID in 'sub' claim
    const token = await new jose.SignJWT({
      sub: userId,
      email: email,
      userId: userId
    })
      .setProtectedHeader({ alg: 'HS256' })
      .setIssuedAt()
      .setExpirationTime('7d')
      .sign(secret);

    return token;
  } catch (error) {
    console.error('Error generating JWT token:', error);
    // Re-throw with more specific error message
    if (error instanceof Error && error.message.includes('No active session')) {
      throw new Error('Authentication required - no active session found');
    }
    throw new Error(`Failed to generate authentication token: ${(error as Error).message}`);
  }
}

/**
 * Verify JWT token and extract user ID (for server-side use).
 * This is useful when you need to verify the token on the frontend server components.
 */
export async function verifyJwtToken(token: string): Promise<string | null> {
  try {
    const secret = new TextEncoder().encode(
      process.env.JWT_SECRET || process.env.BETTER_AUTH_SECRET || 'development-secret-key'
    );

    const { payload } = await jose.jwtVerify(token, secret);
    const payloadObj = payload as Record<string, unknown>;
    return (
      (payloadObj.sub as string) ||
      (payloadObj.userId as string) ||
      ((payloadObj.user as Record<string, unknown>)?.id as string) ||
      null
    );
  } catch (error) {
    console.error('JWT verification failed:', error);
    return null;
  }
}