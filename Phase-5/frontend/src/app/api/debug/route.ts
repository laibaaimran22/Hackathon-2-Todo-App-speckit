import { NextRequest } from 'next/server';
import { cookies } from 'next/headers';

export async function GET(request: NextRequest) {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    const jwtSecret = process.env.JWT_SECRET ? 'SET' : 'NOT_SET';
    const betterAuthSecret = process.env.BETTER_AUTH_SECRET ? 'SET' : 'NOT_SET';
    
    // Get auth cookie
    const cookieStore = await cookies();
    const authToken = cookieStore.get('auth-token');
    const betterAuthSession = cookieStore.getAll().filter(c => c.name.includes('auth') || c.name.includes('session'));
    
    // Test connection to backend
    let backendStatus = 'UNKNOWN';
    let backendError = '';
    let backendHealthCheck = null;
    
    if (!apiUrl) {
      backendStatus = 'ERROR';
      backendError = 'NEXT_PUBLIC_API_URL not configured';
    } else {
      try {
        const response = await fetch(`${apiUrl}/health`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });
        backendStatus = response.ok ? 'OK' : `HTTP ${response.status}`;
        if (response.ok) {
          backendHealthCheck = await response.json();
        }
      } catch (e) {
        backendStatus = 'ERROR';
        backendError = (e as Error).message;
      }
    }

    // Test CORS
    let corsStatus = 'UNKNOWN';
    let corsError = '';
    if (apiUrl) {
      try {
        const response = await fetch(`${apiUrl}/api/tasks`, {
          method: 'OPTIONS',
          headers: { 
            'Content-Type': 'application/json',
            'Origin': process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'
          }
        });
        corsStatus = response.ok ? 'OK' : `HTTP ${response.status}`;
      } catch (e) {
        corsStatus = 'ERROR';
        corsError = (e as Error).message;
      }
    }

    return Response.json({
      timestamp: new Date().toISOString(),
      environment: {
        NEXT_PUBLIC_API_URL: apiUrl,
        NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
        JWT_SECRET: jwtSecret,
        BETTER_AUTH_SECRET: betterAuthSecret,
        NODE_ENV: process.env.NODE_ENV
      },
      cookies: {
        authToken: authToken ? 'PRESENT' : 'MISSING',
        betterAuthCookies: betterAuthSession.map(c => c.name)
      },
      backend: {
        status: backendStatus,
        error: backendError,
        url: apiUrl,
        healthCheck: backendHealthCheck
      },
      cors: {
        status: corsStatus,
        error: corsError
      }
    });
  } catch (error) {
    return Response.json({ 
      error: 'Debug endpoint failed',
      message: (error as Error).message 
    }, { status: 500 });
  }
}
