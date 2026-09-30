import 'server-only';
import { decrypt, encrypt } from '../crypto';
import { env } from '../env';
import { db, must } from '../supabase';

// calendar.events: read and write events (and watch them).
// calendar.calendarlist.readonly: list the calendars an account can see.
export const GOOGLE_SCOPES = [
  'openid',
  'email',
  'https://www.googleapis.com/auth/calendar.events',
  'https://www.googleapis.com/auth/calendar.calendarlist.readonly',
];

export const redirectUri = () => `${env.appUrl}/api/google/callback`;

export function authorizeUrl(state: string, loginHint?: string): string {
  const url = new URL('https://accounts.google.com/o/oauth2/v2/auth');
  url.search = new URLSearchParams({
    client_id: env.googleClientId,
    redirect_uri: redirectUri(),
    response_type: 'code',
    scope: GOOGLE_SCOPES.join(' '),
    access_type: 'offline',
    // Always ask, so Google always returns a refresh token.
    prompt: 'consent select_account',
    include_granted_scopes: 'true',
    state,
    ...(loginHint ? { login_hint: loginHint } : {}),
  }).toString();
  return url.toString();
}

interface TokenResponse {
  access_token: string;
  expires_in: number;
  refresh_token?: string;
  scope?: string;
  error?: string;
  error_description?: string;
}

async function tokenRequest(params: Record<string, string>): Promise<TokenResponse> {
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id: env.googleClientId, client_secret: env.googleClientSecret, ...params }),
  });
  const body = (await res.json()) as TokenResponse;
  if (!res.ok) throw new OAuthError(body.error ?? `http_${res.status}`, body.error_description ?? 'Token request failed');
  return body;
}

export class OAuthError extends Error {
  constructor(public code: string, message: string) {
    super(`${code}: ${message}`);
  }
}

export async function exchangeCode(code: string) {
  const tokens = await tokenRequest({ code, grant_type: 'authorization_code', redirect_uri: redirectUri() });
  const info = await fetch('https://openidconnect.googleapis.com/v1/userinfo', {
    headers: { authorization: `Bearer ${tokens.access_token}` },
  }).then((r) => r.json() as Promise<{ email?: string }>);
  if (!info.email) throw new Error('Google did not return an email address for this account.');
  return { email: info.email.toLowerCase(), tokens };
}

// Store a freshly connected account. Reconnecting the same email replaces its tokens.
export async function saveAccount(email: string, tokens: TokenResponse): Promise<string> {
  const existing = await db().from('google_accounts').select('id, refresh_token_enc').eq('email', email).maybeSingle();
  const refresh = tokens.refresh_token ?? (existing.data ? decrypt(existing.data.refresh_token_enc) : null);
  if (!refresh) throw new Error('Google did not return a refresh token. Remove the app from your Google account permissions and connect again.');
  const row = {
    email,
    refresh_token_enc: encrypt(refresh),
    access_token_enc: encrypt(tokens.access_token),
    access_token_expires_at: new Date(Date.now() + (tokens.expires_in - 60) * 1000).toISOString(),
    scopes: tokens.scope ?? null,
    status: 'active',
    last_error: null,
    updated_at: new Date().toISOString(),
  };
  const saved = must(await db().from('google_accounts').upsert(row, { onConflict: 'email' }).select('id').single(), 'save account');
  return saved.id as string;
}

interface AccountTokens {
  id: string;
  email: string;
  refresh_token_enc: string;
  access_token_enc: string | null;
  access_token_expires_at: string | null;
}

const memo = new Map<string, { token: string; expires: number }>();

export async function accessToken(accountId: string): Promise<string> {
  const cached = memo.get(accountId);
  if (cached && cached.expires > Date.now()) return cached.token;

  const acct = must(
    await db().from('google_accounts').select('id, email, refresh_token_enc, access_token_enc, access_token_expires_at').eq('id', accountId).single(),
    'load account',
  ) as AccountTokens;
  if (acct.access_token_enc && acct.access_token_expires_at && new Date(acct.access_token_expires_at).getTime() > Date.now() + 30_000) {
    const token = decrypt(acct.access_token_enc);
    memo.set(accountId, { token, expires: new Date(acct.access_token_expires_at).getTime() - 30_000 });
    return token;
  }

  try {
    const tokens = await tokenRequest({ grant_type: 'refresh_token', refresh_token: decrypt(acct.refresh_token_enc) });
    const expires = Date.now() + (tokens.expires_in - 60) * 1000;
    await db()
      .from('google_accounts')
      .update({
        access_token_enc: encrypt(tokens.access_token),
        access_token_expires_at: new Date(expires).toISOString(),
        ...(tokens.refresh_token ? { refresh_token_enc: encrypt(tokens.refresh_token) } : {}),
        status: 'active',
        last_error: null,
        updated_at: new Date().toISOString(),
      })
      .eq('id', accountId);
    memo.set(accountId, { token: tokens.access_token, expires });
    return tokens.access_token;
  } catch (err) {
    if (err instanceof OAuthError && err.code === 'invalid_grant') {
      await db()
        .from('google_accounts')
        .update({ status: 'error', last_error: 'Google revoked access. Reconnect this account.', updated_at: new Date().toISOString() })
        .eq('id', accountId);
    }
    throw err;
  }
}

export async function revoke(refreshTokenEnc: string): Promise<void> {
  await fetch(`https://oauth2.googleapis.com/revoke?token=${encodeURIComponent(decrypt(refreshTokenEnc))}`, { method: 'POST' }).catch(() => undefined);
}
