import 'server-only';
import { getCalendars, log } from '../data';
import { db } from '../supabase';
import { reconcileSource, type ReconcileResult } from './reconcile';
import { renewWatches } from './watch';

const LOCK_SECONDS = 280;
const MAX_PASSES = 3;

// Run reconcileSource under a per-calendar lock. If a webhook arrives while a
// pass is running, the holder notices the dirty flag and runs once more, so
// bursts of notifications collapse into at most a couple of passes.
export async function syncCalendar(calendarId: string, reason: string): Promise<ReconcileResult | null> {
  let last: ReconcileResult | null = null;
  for (let pass = 0; pass < MAX_PASSES; pass++) {
    const { data: locked, error } = await db().rpc('try_lock_calendar', { p_calendar_id: calendarId, p_seconds: LOCK_SECONDS });
    if (error) throw new Error(`lock: ${error.message}`);
    if (!locked) return last; // Another run holds it and will pick this up.
    let dirty = false;
    try {
      last = await reconcileSource(calendarId);
    } catch (err) {
      const message = (err as Error).message;
      await db().from('calendars').update({ last_sync_error: message }).eq('id', calendarId);
      await log({ level: 'error', action: 'sync', calendar_id: calendarId, message, details: { reason } });
    } finally {
      const { data } = await db().rpc('unlock_calendar', { p_calendar_id: calendarId });
      dirty = Boolean(data);
    }
    if (!dirty) break;
  }
  return last;
}

export async function syncAll(reason: string, opts: { renew?: boolean } = {}) {
  const calendars = await getCalendars();
  if (opts.renew) await renewWatches(calendars);
  const results = [];
  // Disabled calendars are synced too: that is how their mirrors get cleaned up.
  for (const cal of calendars) results.push(await syncCalendar(cal.id, reason));
  return results.filter(Boolean) as ReconcileResult[];
}
