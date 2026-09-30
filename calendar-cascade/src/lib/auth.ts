import 'server-only';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { env } from './env';
import { SESSION_COOKIE, verifySessionToken } from './session';

// Server actions are reachable from any route, including ones the proxy lets
// through, so every action checks the session itself.
export async function requireSession(): Promise<void> {
  const token = (await cookies()).get(SESSION_COOKIE)?.value;
  if (!(await verifySessionToken(token, env.sessionSecret))) redirect('/login');
}
