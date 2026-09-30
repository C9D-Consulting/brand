import { defaultRule } from '@/lib/engine/policy';
import type { CalendarRow, Detail, GEvent, RuleRow } from '@/lib/engine/types';

export function cal(id: string, label: string, opts: { out?: Detail; inMax?: Detail } = {}): CalendarRow {
  return {
    id,
    account_id: `acct-${id}`,
    google_calendar_id: `${id}@example.com`,
    label,
    color: '#d6743a',
    time_zone: 'America/Chicago',
    enabled: true,
    outbound_detail: opts.out ?? 'full',
    inbound_max_detail: opts.inMax ?? 'full',
    sort_order: 0,
    watch_channel_id: null,
    watch_resource_id: null,
    watch_expires_at: null,
    last_synced_at: null,
    last_sync_error: null,
    created_at: '2026-09-01T00:00:00Z',
  };
}

export function rule(source: CalendarRow, target: CalendarRow, over: Partial<RuleRow> = {}): RuleRow {
  return { id: `${source.id}->${target.id}`, ...defaultRule(source, target), ...over };
}

export function event(over: Partial<GEvent> = {}): GEvent {
  return {
    id: 'evt1',
    status: 'confirmed',
    summary: 'Quarterly planning',
    description: 'Agenda: roadmap',
    location: 'Room 4',
    start: { dateTime: '2026-10-01T10:00:00-05:00', timeZone: 'America/Chicago' },
    end: { dateTime: '2026-10-01T11:00:00-05:00', timeZone: 'America/Chicago' },
    iCalUID: 'evt1@google.com',
    hangoutLink: 'https://meet.google.com/abc-defg-hij',
    organizer: { email: 'boss@sayer.com', displayName: 'The Boss' },
    attendees: [
      { email: 'brandon@sayer.com', self: true, responseStatus: 'accepted' },
      { email: 'peer@sayer.com', displayName: 'Peer', responseStatus: 'tentative' },
    ],
    ...over,
  };
}

// The four calendars from the brief. Sayer (the employer) only ever receives busy blocks.
export const sayer = cal('sayer', 'Sayer', { inMax: 'busy' });
export const c9d = cal('c9d', 'C9D Consulting');
export const mk = cal('mk', 'MonetizeKit');
export const pro = cal('pro', 'Brandon.Wilburn.Pro');
export const all = [sayer, c9d, mk, pro];
export const calendarMap = new Map(all.map((c) => [c.id, c]));
