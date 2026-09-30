import { NextResponse, type NextRequest } from 'next/server';
import { safeEqual } from '@/lib/crypto';
import { log } from '@/lib/data';
import { exchangeCode, saveAccount } from '@/lib/google/oauth';

export async function GET(request: NextRequest) {
  const params = request.nextUrl.searchParams;
  const back = (query: Record<string, string>) => {
    const url = new URL('/calendars', request.url);
    for (const [k, v] of Object.entries(query)) url.searchParams.set(k, v);
    const res = NextResponse.redirect(url);
    res.cookies.delete({ name: 'cc_oauth_state', path: '/api/google' });
    return res;
  };

  if (params.get('error')) return back({ error: `Google said: ${params.get('error')}` });
  const state = request.cookies.get('cc_oauth_state')?.value;
  const code = params.get('code');
  if (!state || !code || !safeEqual(state, params.get('state') ?? '')) {
    return back({ error: 'The sign-in link expired. Try connecting again.' });
  }

  try {
    const { email, tokens } = await exchangeCode(code);
    const id = await saveAccount(email, tokens);
    await log({ action: 'account.connect', message: `Connected ${email}.` });
    return back({ account: id });
  } catch (err) {
    return back({ error: (err as Error).message });
  }
}
