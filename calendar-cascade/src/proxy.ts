import { NextResponse, type NextRequest } from 'next/server';
import { SESSION_COOKIE, verifySessionToken } from '@/lib/session';

// Everything is behind the dashboard sign-in except the sign-in page itself and
// the machine endpoints, which authenticate on their own (channel token, cron secret).
export async function proxy(request: NextRequest) {
  const ok = await verifySessionToken(request.cookies.get(SESSION_COOKIE)?.value, process.env.SESSION_SECRET);
  if (ok) return NextResponse.next();
  if (request.nextUrl.pathname.startsWith('/api/')) {
    return NextResponse.json({ error: 'unauthorized' }, { status: 401 });
  }
  const login = new URL('/login', request.url);
  login.searchParams.set('next', request.nextUrl.pathname);
  return NextResponse.redirect(login);
}

export const config = {
  matcher: ['/((?!login|api/google/webhook|api/cron|_next/static|_next/image|favicon.ico|icon.svg).*)'],
};
