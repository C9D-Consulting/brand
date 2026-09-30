import { after, NextResponse, type NextRequest } from 'next/server';
import { db } from '@/lib/supabase';
import { syncCalendar } from '@/lib/sync/runner';
import { verifyChannelToken } from '@/lib/sync/watch';

export const maxDuration = 300;

// Google push notification: "something changed on this calendar". It carries
// no event data, so we answer at once and reconcile the calendar afterwards.
export async function POST(request: NextRequest) {
  const channelId = request.headers.get('x-goog-channel-id');
  const state = request.headers.get('x-goog-resource-state');
  if (!channelId || !verifyChannelToken(channelId, request.headers.get('x-goog-channel-token'))) {
    return NextResponse.json({ error: 'unknown channel' }, { status: 401 });
  }

  const { data: cal } = await db().from('calendars').select('id').eq('watch_channel_id', channelId).maybeSingle();
  // A channel we replaced may still fire until it expires; ignore it quietly.
  if (!cal) return new NextResponse(null, { status: 200 });
  if (state === 'sync') return new NextResponse(null, { status: 200 });

  after(() => syncCalendar(cal.id, 'webhook'));
  return new NextResponse(null, { status: 200 });
}
