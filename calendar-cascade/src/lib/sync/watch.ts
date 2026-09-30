import 'server-only';
import { randomUUID } from 'node:crypto';
import { hmac, safeEqual } from '../crypto';
import type { CalendarRow } from '../engine/types';
import { env } from '../env';
import { log } from '../data';
import { stopChannel, watchEvents } from '../google/calendar';
import { accessToken } from '../google/oauth';
import { db } from '../supabase';

// Google push notifications. A channel lives at most about a week, so the cron
// renews any that expire within RENEW_BEFORE.
const TTL_SECONDS = 7 * 24 * 3600;
const RENEW_BEFORE_MS = 48 * 3600 * 1000;

export const channelToken = (channelId: string) => hmac(`channel:${channelId}`);
export const verifyChannelToken = (channelId: string, token: string | null) => Boolean(token) && safeEqual(channelToken(channelId), token!);

export function webhooksAvailable(): boolean {
  return env.appUrl.startsWith('https://');
}

export async function startWatch(cal: CalendarRow): Promise<void> {
  if (!webhooksAvailable()) return; // Local dev: rely on "Sync now" and the cron.
  const token = await accessToken(cal.account_id);
  const id = randomUUID();
  const channel = await watchEvents(token, cal.google_calendar_id, {
    id,
    address: `${env.appUrl}/api/google/webhook`,
    token: channelToken(id),
    ttlSeconds: TTL_SECONDS,
  });
  const previous = { id: cal.watch_channel_id, resourceId: cal.watch_resource_id };
  await db()
    .from('calendars')
    .update({
      watch_channel_id: channel.id,
      watch_resource_id: channel.resourceId,
      watch_expires_at: channel.expiration ? new Date(Number(channel.expiration)).toISOString() : new Date(Date.now() + TTL_SECONDS * 1000).toISOString(),
    })
    .eq('id', cal.id);
  if (previous.id && previous.resourceId) await stopChannel(token, previous.id, previous.resourceId);
}

export async function stopWatch(cal: CalendarRow): Promise<void> {
  if (!cal.watch_channel_id || !cal.watch_resource_id) return;
  try {
    await stopChannel(await accessToken(cal.account_id), cal.watch_channel_id, cal.watch_resource_id);
  } catch (err) {
    await log({ level: 'warn', action: 'watch.stop', calendar_id: cal.id, message: (err as Error).message });
  }
  await db().from('calendars').update({ watch_channel_id: null, watch_resource_id: null, watch_expires_at: null }).eq('id', cal.id);
}

export async function renewWatches(calendars: CalendarRow[]): Promise<void> {
  for (const cal of calendars) {
    const due = !cal.watch_expires_at || new Date(cal.watch_expires_at).getTime() - Date.now() < RENEW_BEFORE_MS;
    try {
      if (cal.enabled && due) await startWatch(cal);
      if (!cal.enabled && cal.watch_channel_id) await stopWatch(cal);
    } catch (err) {
      await log({ level: 'error', action: 'watch.renew', calendar_id: cal.id, message: `${cal.label}: ${(err as Error).message}` });
    }
  }
}
