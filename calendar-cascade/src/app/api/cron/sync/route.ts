import { NextResponse, type NextRequest } from 'next/server';
import { safeEqual } from '@/lib/crypto';
import { env } from '@/lib/env';
import { syncAll } from '@/lib/sync/runner';

export const maxDuration = 300;

// Safety net behind the webhooks: renew expiring watch channels and reconcile
// every calendar. Vercel Cron calls this with Authorization: Bearer $CRON_SECRET.
export async function GET(request: NextRequest) {
  const secret = env.cronSecret;
  const given = request.headers.get('authorization') ?? '';
  if (!secret || !safeEqual(given, `Bearer ${secret}`)) {
    return NextResponse.json({ error: 'unauthorized' }, { status: 401 });
  }
  const results = await syncAll('cron', { renew: true });
  return NextResponse.json({ ok: true, results });
}
