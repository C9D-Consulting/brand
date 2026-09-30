'use server';

import { after } from 'next/server';
import { cookies } from 'next/headers';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { requireSession } from '@/lib/auth';
import { safeEqual } from '@/lib/crypto';
import { getCalendar, getCalendars, getRule, getRules, log } from '@/lib/data';
import { defaultRule } from '@/lib/engine/policy';
import { DETAILS, type CalendarRow, type Detail, type RuleRow } from '@/lib/engine/types';
import { env } from '@/lib/env';
import { revoke } from '@/lib/google/oauth';
import { createSessionToken, SESSION_COOKIE, SESSION_TTL_SECONDS } from '@/lib/session';
import { db, must } from '@/lib/supabase';
import { purgeMirrors } from '@/lib/sync/reconcile';
import { syncAll, syncCalendar } from '@/lib/sync/runner';
import { startWatch, stopWatch } from '@/lib/sync/watch';

const str = (f: FormData, k: string) => String(f.get(k) ?? '').trim();
const bool = (f: FormData, k: string) => f.get(k) === 'on' || f.get(k) === 'true';
const int = (f: FormData, k: string, min: number, max: number) => Math.min(max, Math.max(min, Math.round(Number(f.get(k)) || 0)));
const detail = (v: string, fallback: Detail): Detail => ((DETAILS as string[]).includes(v) ? (v as Detail) : fallback);

function refresh() {
  revalidatePath('/', 'layout');
}

// ---------- session ----------

export async function login(_: unknown, form: FormData): Promise<{ error?: string }> {
  if (!safeEqual(str(form, 'password'), env.adminPassword)) {
    await new Promise((r) => setTimeout(r, 600));
    return { error: 'That password is not right.' };
  }
  (await cookies()).set(SESSION_COOKIE, await createSessionToken(env.sessionSecret), {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: SESSION_TTL_SECONDS,
    path: '/',
  });
  const next = str(form, 'next');
  redirect(next.startsWith('/') && !next.startsWith('//') ? next : '/');
}

export async function logout() {
  (await cookies()).delete(SESSION_COOKIE);
  redirect('/login');
}

// ---------- calendars ----------

// Create any missing rule between enabled pairs, using each calendar's policy.
async function ensureRules(calendars: CalendarRow[]) {
  const have = new Set((await getRules()).map((r) => `${r.source_calendar_id}>${r.target_calendar_id}`));
  const missing = calendars.flatMap((s) =>
    calendars.filter((t) => t.id !== s.id && !have.has(`${s.id}>${t.id}`)).map((t) => defaultRule(s, t)),
  );
  if (missing.length) must(await db().from('rules').insert(missing), 'create rules');
}

export async function addCalendar(form: FormData) {
  await requireSession();
  const row = {
    account_id: str(form, 'account_id'),
    google_calendar_id: str(form, 'google_calendar_id'),
    label: str(form, 'label') || str(form, 'google_calendar_id'),
    color: str(form, 'color') || '#d6743a',
    time_zone: str(form, 'time_zone') || null,
    outbound_detail: detail(str(form, 'outbound_detail'), 'full'),
    inbound_max_detail: detail(str(form, 'inbound_max_detail'), 'full'),
    sort_order: (await getCalendars()).length,
  };
  const cal = must(await db().from('calendars').insert(row).select('*').single(), 'add calendar') as CalendarRow;
  await ensureRules(await getCalendars());
  await log({ action: 'calendar.add', calendar_id: cal.id, message: `Added ${cal.label}. Rules to and from every other calendar were created from its policy.` });
  after(async () => {
    try {
      await startWatch(cal);
    } catch (err) {
      await log({ level: 'error', action: 'watch.start', calendar_id: cal.id, message: (err as Error).message });
    }
    await syncAll('calendar added');
  });
  refresh();
}

export async function updateCalendar(form: FormData) {
  await requireSession();
  const id = str(form, 'id');
  const before = await getCalendar(id);
  if (!before) return;
  const patch = {
    label: str(form, 'label') || before.label,
    color: str(form, 'color') || before.color,
    enabled: bool(form, 'enabled'),
    outbound_detail: detail(str(form, 'outbound_detail'), before.outbound_detail),
    inbound_max_detail: detail(str(form, 'inbound_max_detail'), before.inbound_max_detail),
    sort_order: int(form, 'sort_order', 0, 999),
    updated_at: new Date().toISOString(),
  };
  const cal = must(await db().from('calendars').update(patch).eq('id', id).select('*').single(), 'update calendar') as CalendarRow;
  await log({ action: 'calendar.update', calendar_id: id, message: `Updated ${cal.label}.` });
  after(async () => {
    if (cal.enabled && !before.enabled) await startWatch(cal).catch(() => undefined);
    if (!cal.enabled && before.enabled) await stopWatch(cal);
    // Labels, ceilings and enablement change what other calendars write, so sync everything.
    await syncAll('calendar updated');
  });
  refresh();
}

export async function removeCalendar(form: FormData) {
  await requireSession();
  const id = str(form, 'id');
  const cal = await getCalendar(id);
  if (!cal) return;
  await stopWatch(cal);
  let purged = 0;
  if (bool(form, 'purge')) {
    purged += await purgeMirrors({ sourceId: id });
    purged += await purgeMirrors({ targetId: id });
  }
  must(await db().from('calendars').delete().eq('id', id), 'remove calendar');
  await log({ action: 'calendar.remove', message: `Removed ${cal.label}${purged ? ` and ${purged} mirrored events` : ''}.` });
  refresh();
}

export async function removeAccount(form: FormData) {
  await requireSession();
  const id = str(form, 'id');
  const acct = must(await db().from('google_accounts').select('id, email, refresh_token_enc').eq('id', id).single(), 'load account') as {
    email: string;
    refresh_token_enc: string;
  };
  for (const cal of (await getCalendars()).filter((c) => c.account_id === id)) {
    await stopWatch(cal);
    await purgeMirrors({ sourceId: cal.id });
    await purgeMirrors({ targetId: cal.id });
  }
  await revoke(acct.refresh_token_enc);
  must(await db().from('google_accounts').delete().eq('id', id), 'remove account');
  await log({ action: 'account.remove', message: `Disconnected ${acct.email} and removed its mirrors.` });
  refresh();
}

// ---------- rules ----------

export async function setRuleDetail(form: FormData) {
  await requireSession();
  const id = str(form, 'id');
  const value = str(form, 'value');
  const patch = value === 'off' ? { enabled: false } : { enabled: true, detail: detail(value, 'busy') };
  const rule = must(await db().from('rules').update({ ...patch, updated_at: new Date().toISOString() }).eq('id', id).select('*').single(), 'update rule') as RuleRow;
  after(() => syncCalendar(rule.source_calendar_id, 'rule changed'));
  refresh();
}

export async function saveRule(form: FormData) {
  await requireSession();
  const id = str(form, 'id');
  const before = await getRule(id);
  if (!before) return;
  const patch: Partial<RuleRow> & { updated_at: string } = {
    enabled: bool(form, 'enabled'),
    detail: detail(str(form, 'detail'), before.detail),
    title_template: str(form, 'title_template') || '{{source}}: {{title}}',
    busy_title: str(form, 'busy_title') || 'Block',
    include_description: bool(form, 'include_description'),
    include_location: bool(form, 'include_location'),
    include_attendees: bool(form, 'include_attendees'),
    include_conference: bool(form, 'include_conference'),
    visibility: (['default', 'public', 'private'].includes(str(form, 'visibility')) ? str(form, 'visibility') : 'default') as RuleRow['visibility'],
    show_as: str(form, 'show_as') === 'free' ? 'free' : 'busy',
    color_id: /^([1-9]|1[01])$/.test(str(form, 'color_id')) ? str(form, 'color_id') : null,
    keep_reminders: bool(form, 'keep_reminders'),
    buffer_before_min: int(form, 'buffer_before_min', 0, 240),
    buffer_after_min: int(form, 'buffer_after_min', 0, 240),
    buffer_title: str(form, 'buffer_title') || 'Buffer',
    skip_all_day: bool(form, 'skip_all_day'),
    skip_free: bool(form, 'skip_free'),
    skip_declined: bool(form, 'skip_declined'),
    skip_tentative: bool(form, 'skip_tentative'),
    skip_if_native_on_target: bool(form, 'skip_if_native_on_target'),
    exclude_keywords: str(form, 'exclude_keywords').split(',').map((s) => s.trim()).filter(Boolean),
    lookahead_days: int(form, 'lookahead_days', 1, 365),
    updated_at: new Date().toISOString(),
  };
  must(await db().from('rules').update(patch).eq('id', id), 'save rule');
  await log({ action: 'rule.update', rule_id: id, calendar_id: before.source_calendar_id, message: 'Rule saved.' });
  after(() => syncCalendar(before.source_calendar_id, 'rule saved'));
  refresh();
  redirect('/?saved=1');
}

// Re-derive every rule's detail from calendar policy. Templates, buffers and
// filters are kept; only on/off and detail level are reset.
export async function resetMatrix() {
  await requireSession();
  const calendars = await getCalendars();
  await ensureRules(calendars);
  const byId = new Map(calendars.map((c) => [c.id, c]));
  for (const rule of await getRules()) {
    const s = byId.get(rule.source_calendar_id);
    const t = byId.get(rule.target_calendar_id);
    if (!s || !t) continue;
    const want = defaultRule(s, t);
    if (rule.detail !== want.detail || !rule.enabled) {
      await db().from('rules').update({ detail: want.detail, enabled: true, updated_at: new Date().toISOString() }).eq('id', rule.id);
    }
  }
  await log({ action: 'rules.reset', message: 'Reset the cascade matrix from calendar policies.' });
  after(() => syncAll('matrix reset'));
  refresh();
}

// ---------- sync ----------

export async function syncNow(form: FormData) {
  await requireSession();
  const id = str(form, 'id');
  if (id) await syncCalendar(id, 'manual');
  else await syncAll('manual', { renew: true });
  refresh();
}
