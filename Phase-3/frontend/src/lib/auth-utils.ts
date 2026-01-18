'use server';

import { cookies } from 'next/headers';

/**
 * Get the JWT token that was stored during login.
 * The token is generated during authentication and stored in cookies.
 * This is simpler and more reliable than trying to generate a new token.
 */
export async function getJwtToken(): Promise<string> {
  try {
    const cookieStore = await cookies();
    
    // Try to get the JWT token from cookies (stored during login)
    // The token format is from the backend's sign-in/email response
    const token = cookieStore.get('auth-token')?.value;

    if (!token) {
      console.error('[AUTH] No auth-token found in cookies');
      throw new Error('Authentication required - no token found');
    }

    // Verify the token is not empty and looks like a JWT (has dots)
    if (!token.includes('.')) {
      console.error('[AUTH] Token does not appear to be a valid JWT');
      throw new Error('Invalid authentication token format');
    }

    console.log('[AUTH] Successfully retrieved JWT token from cookies');
    return token;
  } catch (error) {
    console.error('[AUTH] Error getting JWT token:', error);
    throw new Error(`Failed to get authentication token: ${(error as Error).message}`);
  }
}