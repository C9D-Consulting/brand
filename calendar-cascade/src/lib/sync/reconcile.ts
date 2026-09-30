import 'server-only';
import { isManaged, PROP } from '../engine/mirror';
import { diff, planSource, type DesiredMirror, type Op } from '../engine/plan';
import type { CalendarRow, GEvent, MirrorRow, RuleRow } from '../engine/types';
import { getCalendars, getMirrorsForSource, getRulesForSource, log } from '../data';
import { deleteEvent, GoogleApiError, insertEvent, listEvents, updateEvent } from '../google/calendar';
import { accessToken } from '../google/oauth';
import { db, must } from '../supabase';

const DAY = 86_400_000;

export interface ReconcileResult {
  calendarId: string;
  created: number;
  updated: number;
  deleted: number;
  orphansRemoved: number;
  skipped: number;
  errors: string[];
}

// Bring every mirror of one source calendar in line with its rules.
//
// Idempotent by construction: list the source window, compute the desired
// mirrors, compare with the mirrors table (and with what is really on each
// target), then create, update or delete the difference. Safe to run as often
// as webhooks fire; a no-op run makes no writes.
export async function reconcileSource(sourceId: string, now = new Date()): Promise<ReconcileResult> {
  const result: ReconcileResult = { calendarId: sourceId, created: 0, updated: 0, deleted: 0, orphansRemoved: 0, skipped: 0, errors: [] };
  const calendars = await getCalendars();
  const byId = new Map(calendars.map((c) => [c.id, c]));
  const source = byId.get(sourceId);
  if (!source) return result;

  const rules = (await getRulesForSource(sourceId)).filter((r) => {
    const target = byId.get(r.target_calendar_id);
    return r.enabled && source.enabled && target?.enabled;
  });

  const windowStart = new Date(Math.floor(now.getTime() / DAY) * DAY - DAY);
  const lookahead = Math.max(1, ...rules.map((r) => r.lookahead_days));
  const windowEnd = new Date(now.getTime() + lookahead * DAY);

  // 1. What is on the source.
  let events: GEvent[] = [];
  if (rules.length) {
    events = await listEvents(await accessToken(source.account_id), source.google_calendar_id, windowStart, windowEnd);
  }
  const listed = new Set(events.map((e) => e.id));

  // 2. What we already wrote (a little before the window, so ongoing events match).
  const existing = await getMirrorsForSource(sourceId, new Date(windowStart.getTime() - 2 * DAY));

  // 3. What is on each target: native invitations (to skip) and our own events
  //    (to spot mirrors deleted by hand, and strays left by an interrupted run).
  const targetIds = new Set([...rules.map((r) => r.target_calendar_id), ...existing.map((m) => m.target_calendar_id)]);
  const native = new Map<string, Set<string>>();
  const present = new Map<string, Set<string>>();
  const ours = new Map<string, GEvent[]>();
  const unreachable = new Set<string>();
  for (const id of targetIds) {
    const target = byId.get(id);
    if (!target) continue;
    try {
      const token = await accessToken(target.account_id);
      const items = await listEvents(token, target.google_calendar_id, new Date(windowStart.getTime() - DAY), new Date(windowEnd.getTime() + DAY));
      native.set(id, new Set(items.filter((e) => !isManaged(e) && e.iCalUID).map((e) => e.iCalUID!)));
      present.set(id, new Set(items.map((e) => e.id)));
      ours.set(id, items.filter((e) => isManaged(e) && e.extendedProperties?.private?.[PROP.sourceCalendar] === sourceId));
    } catch (err) {
      unreachable.add(id);
      result.errors.push(`${target.label}: ${(err as Error).message}`);
    }
  }

  // 4. Plan and diff. Rules whose target could not be read are left untouched.
  const activeRules = rules.filter((r) => !unreachable.has(r.target_calendar_id));
  const plan = planSource({ source, rules: activeRules, calendars: byId, events, now, nativeICalUIDs: native });
  result.skipped = plan.skipped.length;
  const ops = diff({
    desired: plan.desired,
    existing: existing.filter((m) => !unreachable.has(m.target_calendar_id)),
    listedSourceEventIds: listed,
    windowStart,
    presentOnTarget: present,
  });

  // 5. Apply.
  for (const op of ops) {
    try {
      await apply(op, byId);
      if (op.type === 'create') result.created++;
      else if (op.type === 'delete') result.deleted++;
      else result.updated++;
    } catch (err) {
      const msg = (err as Error).message;
      result.errors.push(msg);
      await log({
        level: 'error',
        action: `mirror.${op.type}`,
        calendar_id: sourceId,
        rule_id: 'want' in op ? op.want.ruleId : op.have.rule_id,
        message: msg,
      });
    }
  }

  // 6. Strays: events carrying our marker for this source that no mirror row
  //    points at (a run that died between the Google write and the DB insert).
  result.orphansRemoved = await removeStrays(sourceId, ours, byId);

  await db()
    .from('calendars')
    .update({ last_synced_at: new Date().toISOString(), last_sync_error: result.errors[0] ?? null })
    .eq('id', sourceId);

  const changed = result.created + result.updated + result.deleted + result.orphansRemoved;
  if (changed || result.errors.length) {
    await log({
      level: result.errors.length ? 'warn' : 'info',
      action: 'sync',
      calendar_id: sourceId,
      message: `${source.label}: ${result.created} created, ${result.updated} updated, ${result.deleted} removed${result.orphansRemoved ? `, ${result.orphansRemoved} strays cleaned` : ''}${result.errors.length ? `, ${result.errors.length} errors` : ''}.`,
      details: { ...result, skippedReasons: tally(plan.skipped.map((s) => s.reason)) },
    });
  }
  return result;
}

function tally(values: string[]): Record<string, number> {
  const out: Record<string, number> = {};
  for (const v of values) out[v] = (out[v] ?? 0) + 1;
  return out;
}

async function tokenFor(calendarId: string, byId: Map<string, CalendarRow>) {
  const target = byId.get(calendarId);
  if (!target) throw new Error(`Unknown calendar ${calendarId}`);
  return { target, token: await accessToken(target.account_id) };
}

function mirrorRow(want: DesiredMirror, sourceId: string, targetEventId: string) {
  return {
    rule_id: want.ruleId,
    source_calendar_id: sourceId,
    source_event_id: want.sourceEventId,
    target_calendar_id: want.targetCalendarId,
    target_event_id: targetEventId,
    kind: want.kind,
    source_start: want.sourceStart,
    source_end: want.sourceEnd,
    content_hash: want.hash,
    updated_at: new Date().toISOString(),
  };
}

async function apply(op: Op, byId: Map<string, CalendarRow>): Promise<void> {
  if (op.type === 'delete') {
    const { target, token } = await tokenFor(op.have.target_calendar_id, byId);
    await deleteEvent(token, target.google_calendar_id, op.have.target_event_id);
    must(await db().from('mirrors').delete().eq('id', op.have.id), 'delete mirror');
    return;
  }

  const { target, token } = await tokenFor(op.want.targetCalendarId, byId);
  const sourceId = op.want.payload.extendedProperties.private[PROP.sourceCalendar];

  if (op.type === 'update') {
    try {
      await updateEvent(token, target.google_calendar_id, op.have.target_event_id, op.want.payload);
      must(await db().from('mirrors').update(mirrorRow(op.want, sourceId, op.have.target_event_id)).eq('id', op.have.id), 'update mirror');
      return;
    } catch (err) {
      if (!(err instanceof GoogleApiError && err.gone)) throw err;
      // Deleted on the target since we last looked: fall through and recreate.
    }
  }

  const created = await insertEvent(token, target.google_calendar_id, op.want.payload);
  if (op.type === 'create') {
    const res = await db().from('mirrors').insert(mirrorRow(op.want, sourceId, created.id));
    if (res.error) {
      // Keep Google and the table consistent: undo the write we cannot record.
      await deleteEvent(token, target.google_calendar_id, created.id).catch(() => undefined);
      throw new Error(`record mirror: ${res.error.message}`);
    }
  } else {
    must(await db().from('mirrors').update(mirrorRow(op.want, sourceId, created.id)).eq('id', op.have.id), 'update mirror');
  }
}

async function removeStrays(sourceId: string, ours: Map<string, GEvent[]>, byId: Map<string, CalendarRow>): Promise<number> {
  let removed = 0;
  for (const [targetId, events] of ours) {
    if (!events.length) continue;
    const ids = events.map((e) => e.id);
    const known = new Set<string>();
    for (let i = 0; i < ids.length; i += 200) {
      const rows = must(
        await db().from('mirrors').select('target_event_id').eq('target_calendar_id', targetId).in('target_event_id', ids.slice(i, i + 200)),
        'match strays',
      ) as Pick<MirrorRow, 'target_event_id'>[];
      rows.forEach((r) => known.add(r.target_event_id));
    }
    const strays = ids.filter((id) => !known.has(id));
    if (!strays.length) continue;
    const { target, token } = await tokenFor(targetId, byId);
    for (const id of strays) {
      try {
        await deleteEvent(token, target.google_calendar_id, id);
        removed++;
      } catch (err) {
        await log({ level: 'warn', action: 'stray.delete', calendar_id: sourceId, message: (err as Error).message });
      }
    }
  }
  return removed;
}

// Remove every mirror a rule wrote (used when the calendars it joins are removed).
export async function purgeMirrors(filter: { sourceId?: string; targetId?: string; ruleId?: string }): Promise<number> {
  let q = db().from('mirrors').select('*');
  if (filter.sourceId) q = q.eq('source_calendar_id', filter.sourceId);
  if (filter.targetId) q = q.eq('target_calendar_id', filter.targetId);
  if (filter.ruleId) q = q.eq('rule_id', filter.ruleId);
  const rows = must(await q.limit(10000), 'list mirrors') as MirrorRow[];
  const byId = new Map((await getCalendars()).map((c) => [c.id, c]));
  let removed = 0;
  for (const row of rows) {
    try {
      const { target, token } = await tokenFor(row.target_calendar_id, byId);
      await deleteEvent(token, target.google_calendar_id, row.target_event_id);
      await db().from('mirrors').delete().eq('id', row.id);
      removed++;
    } catch (err) {
      await log({ level: 'warn', action: 'purge', calendar_id: row.source_calendar_id, message: (err as Error).message });
    }
  }
  return removed;
}

export type { RuleRow };
