import { NextRequest, NextResponse } from 'next/server';

export async function middleware(request: NextRequest) {
  // Proxy auth requests to backend
  if (request.nextUrl.pathname.startsWith('/api/auth/')) {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL;
    if (backendUrl) {
      const url = new URL(request.url);
      const backend = new URL(backendUrl);

      // Change the host to point to backend
      url.protocol = backend.protocol;
      url.host = backend.host;

      return NextResponse.rewrite(url);
    }
  }

  // Check for our custom auth token cookie instead of Better Auth session
  const authToken = request.cookies.get('auth-token')?.value;
  const isAuthPage = request.nextUrl.pathname.startsWith('/login') ||
                     request.nextUrl.pathname.startsWith('/signup');
  const isDashboardPage = request.nextUrl.pathname.startsWith('/dashboard');

  if (isDashboardPage && !authToken) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (isAuthPage && authToken) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/api/auth/:path*', '/dashboard/:path*', '/login', '/signup'],
};
