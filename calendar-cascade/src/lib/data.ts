import 'server-only';
import type { CalendarRow, MirrorRow, RuleRow } from './engine/types';
import { db, must } from './supabase';

export interface AccountRow {
  id: string;
  email: string;
  status: 'active' | 'error';
  last_error: string | null;
  created_at: string;
}

export interface ActivityRow {
  id: number;
  created_at: string;
  level: 'info' | 'warn' | 'error';
  action: string;
  calendar_id: string | null;
  rule_id: string | null;
  message: string;
  details: Record<string, unknown> | null;
}

export async function getAccounts(): Promise<AccountRow[]> {
  return must(await db().from('google_accounts').select('id, email, status, last_error, created_at').order('created_at'), 'list accounts');
}

export async function getCalendars(): Promise<CalendarRow[]> {
  return must(await db().from('calendars').select('*').order('sort_order').order('created_at'), 'list calendars');
}

export async function getCalendar(id: string): Promise<CalendarRow | null> {
  return must(await db().from('calendars').select('*').eq('id', id).maybeSingle(), 'load calendar');
}

export async function getRules(): Promise<RuleRow[]> {
  return must(await db().from('rules').select('*'), 'list rules');
}

export async function getRule(id: string): Promise<RuleRow | null> {
  return must(await db().from('rules').select('*').eq('id', id).maybeSingle(), 'load rule');
}

export async function getRulesForSource(sourceId: string): Promise<RuleRow[]> {
  return must(await db().from('rules').select('*').eq('source_calendar_id', sourceId), 'list rules');
}

export async function getMirrorsForSource(sourceId: string, endAfter: Date): Promise<MirrorRow[]> {
  const out: MirrorRow[] = [];
  for (let from = 0; ; from += 1000) {
    const page = must(
      await db().from('mirrors').select('*').eq('source_calendar_id', sourceId).gt('source_end', endAfter.toISOString()).order('id').range(from, from + 999),
      'list mirrors',
    ) as MirrorRow[];
    out.push(...page);
    if (page.length < 1000) return out;
  }
}

export async function countMirrors(): Promise<Record<string, number>> {
  // Mirror counts per rule, for the matrix. Small tables; count client side.
  const rows = must(await db().from('mirrors').select('rule_id').gt('source_end', new Date().toISOString()).limit(20000), 'count mirrors') as { rule_id: string }[];
  const counts: Record<string, number> = {};
  for (const r of rows) counts[r.rule_id] = (counts[r.rule_id] ?? 0) + 1;
  return counts;
}

export async function getActivity(limit = 50, calendarId?: string): Promise<ActivityRow[]> {
  let q = db().from('activity').select('*').order('created_at', { ascending: false }).limit(limit);
  if (calendarId) q = q.eq('calendar_id', calendarId);
  return must(await q, 'list activity');
}

export async function log(entry: Omit<ActivityRow, 'id' | 'created_at' | 'details' | 'rule_id' | 'calendar_id' | 'level'> & Partial<ActivityRow>) {
  const { error } = await db().from('activity').insert({ level: 'info', ...entry });
  if (error) console.error('activity log failed', error.message, entry);
}
