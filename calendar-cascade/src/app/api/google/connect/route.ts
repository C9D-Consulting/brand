import { randomBytes } from 'node:crypto';
import { NextResponse, type NextRequest } from 'next/server';
import { authorizeUrl } from '@/lib/google/oauth';

export async function GET(request: NextRequest) {
  const state = randomBytes(24).toString('base64url');
  const res = NextResponse.redirect(authorizeUrl(state, request.nextUrl.searchParams.get('hint') ?? undefined));
  res.cookies.set('cc_oauth_state', state, { httpOnly: true, secure: true, sameSite: 'lax', maxAge: 600, path: '/api/google' });
  return res;
}
