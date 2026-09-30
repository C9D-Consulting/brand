// Single-operator session: a signed, expiring cookie. Uses Web Crypto so the
// same code verifies in proxy.ts and signs in server actions.

export const SESSION_COOKIE = 'cc_session';
export const SESSION_TTL_SECONDS = 60 * 60 * 24 * 30;

async function sign(payload: string, secret: string): Promise<string> {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(payload));
  return Buffer.from(sig).toString('base64url');
}

export async function createSessionToken(secret: string): Promise<string> {
  const exp = Math.floor(Date.now() / 1000) + SESSION_TTL_SECONDS;
  return `${exp}.${await sign(String(exp), secret)}`;
}

export async function verifySessionToken(token: string | undefined, secret: string | undefined): Promise<boolean> {
  if (!token || !secret) return false;
  const [exp, sig] = token.split('.');
  if (!exp || !sig || Number(exp) < Date.now() / 1000) return false;
  const expected = await sign(exp, secret);
  if (expected.length !== sig.length) return false;
  let diff = 0;
  for (let i = 0; i < sig.length; i++) diff |= sig.charCodeAt(i) ^ expected.charCodeAt(i);
  return diff === 0;
}
