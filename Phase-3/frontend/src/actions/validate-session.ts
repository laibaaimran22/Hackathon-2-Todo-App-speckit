'use server'

import * as jose from 'jose';
import { cookies } from 'next/headers';

export async function validateSessionToken(): Promise<boolean> {
  try {
    // We can't access localStorage from server, so we'll need to pass the token as a header
    // This will be called from client components that have access to the token
    return false; // Placeholder - we'll need a different approach
  } catch (error) {
    console.error('Error validating session:', error);
    return false;
  }
}

// Alternative approach: Check if user has a valid token by attempting to validate it
export async function verifyStoredToken(storedToken?: string): Promise<boolean> {
  try {
    if (!storedToken) {
      return false;
    }

    // Attempt to verify the token against the backend
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/user`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${storedToken}`,
        'Content-Type': 'application/json',
      },
    });

    return response.ok;
  } catch (error) {
    console.error('Error verifying stored token:', error);
    return false;
  }
}