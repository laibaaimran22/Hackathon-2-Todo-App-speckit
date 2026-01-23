import { NextRequest, NextResponse } from 'next/server';

export async function middleware(request: NextRequest) {
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
  matcher: ['/dashboard/:path*', '/login', '/signup'],
};
