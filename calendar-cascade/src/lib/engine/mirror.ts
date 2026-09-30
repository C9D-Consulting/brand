// Turns one source event into the event(s) a rule writes to its target calendar.
// Pure: no I/O, safe to import in the browser for live previews.

import { renderTemplate } from './template';
import {
  DETAIL_RANK,
  type CalendarRow,
  type Detail,
  type GEvent,
  type GEventInput,
  type MirrorKind,
  type RuleRow,
} from './types';

// Private extended properties stamped on every event we write. MARKER is how we
// recognise our own events, so a mirror is never cascaded again (no loops).
export const PROP = {
  marker: 'cascade',
  rule: 'cascadeRule',
  sourceCalendar: 'cascadeSourceCalendar',
  sourceEvent: 'cascadeSourceEvent',
  kind: 'cascadeKind',
} as const;

export function isManaged(event: Pick<GEvent, 'extendedProperties'>): boolean {
  return event.extendedProperties?.private?.[PROP.marker] === '1';
}

export function minDetail(...levels: Detail[]): Detail {
  return levels.reduce((low, d) => (DETAIL_RANK[d] < DETAIL_RANK[low] ? d : low));
}

// The detail that actually lands on the target: the rule's choice, capped by the
// target's privacy ceiling, and never more than busy for a private source event.
export function effectiveDetail(
  rule: Pick<RuleRow, 'detail'>,
  target: Pick<CalendarRow, 'inbound_max_detail'>,
  event?: Pick<GEvent, 'visibility'>,
): Detail {
  const eventCap: Detail =
    event?.visibility === 'private' || event?.visibility === 'confidential' ? 'busy' : 'full';
  return minDetail(rule.detail, target.inbound_max_detail, eventCap);
}

export function isAllDay(event: Pick<GEvent, 'start'>): boolean {
  return Boolean(event.start?.date && !event.start?.dateTime);
}

// Start and end as instants. All-day dates are read as UTC midnight, which is
// only used for windowing and bookkeeping, never written back to Google.
export function eventRange(event: Pick<GEvent, 'start' | 'end'>): { start: Date; end: Date } | null {
  const s = event.start?.dateTime ?? (event.start?.date ? `${event.start.date}T00:00:00Z` : null);
  const e = event.end?.dateTime ?? (event.end?.date ? `${event.end.date}T00:00:00Z` : null);
  if (!s || !e) return null;
  const start = new Date(s);
  const end = new Date(e);
  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) return null;
  return { start, end };
}

function selfAttendee(event: GEvent) {
  return event.attendees?.find((a) => a.self);
}

export interface SkipContext {
  horizon?: Date;
  nativeICalUIDs?: Set<string>;
}

// Why a rule would not cascade this event, or null when it should.
export function skipReason(event: GEvent, rule: RuleRow, ctx: SkipContext = {}): string | null {
  if (event.status === 'cancelled') return 'cancelled';
  if (isManaged(event)) return 'written by Calendar Cascade';
  if (event.eventType === 'workingLocation' || event.eventType === 'birthday') {
    return `${event.eventType} event`;
  }
  const range = eventRange(event);
  if (!range) return 'no start or end';
  if (rule.skip_all_day && isAllDay(event)) return 'all-day event';
  if (rule.skip_free && event.transparency === 'transparent') return 'shown as free';
  const me = selfAttendee(event);
  if (rule.skip_declined && me?.responseStatus === 'declined') return 'declined';
  if (rule.skip_tentative && (me?.responseStatus === 'tentative' || me?.responseStatus === 'needsAction')) {
    return 'tentative or not answered';
  }
  const haystack = `${event.summary ?? ''}\n${event.description ?? ''}`.toLowerCase();
  const hit = rule.exclude_keywords.find((k) => k.trim() && haystack.includes(k.trim().toLowerCase()));
  if (hit) return `matches exclude keyword "${hit}"`;
  if (ctx.horizon && range.start >= ctx.horizon) return 'beyond lookahead';
  if (rule.skip_if_native_on_target && event.iCalUID && ctx.nativeICalUIDs?.has(event.iCalUID)) {
    return 'already on target calendar';
  }
  return null;
}

function conferenceLines(event: GEvent): string[] {
  const lines: string[] = [];
  const video = event.conferenceData?.entryPoints?.find((p) => p.entryPointType === 'video')?.uri;
  const join = video ?? event.hangoutLink;
  if (join) lines.push(`Join: ${join}`);
  const phone = event.conferenceData?.entryPoints?.find((p) => p.entryPointType === 'phone');
  if (phone?.uri) lines.push(`Dial-in: ${phone.label ?? phone.uri.replace(/^tel:/, '')}${phone.pin ? ` PIN ${phone.pin}` : ''}`);
  return lines;
}

function attendeeLines(event: GEvent): string[] {
  const lines: string[] = [];
  const organizer = event.organizer?.displayName ?? event.organizer?.email;
  if (organizer) lines.push(`Organizer: ${organizer}`);
  const people = (event.attendees ?? []).filter((a) => !a.resource);
  if (people.length) {
    lines.push('Attendees:');
    for (const a of people.slice(0, 50)) {
      const name = a.displayName ? `${a.displayName} <${a.email ?? ''}>` : (a.email ?? 'unknown');
      const status = a.responseStatus && a.responseStatus !== 'needsAction' ? ` (${a.responseStatus})` : '';
      lines.push(`  - ${name}${status}${a.optional ? ' [optional]' : ''}`);
    }
    if (people.length > 50) lines.push(`  - and ${people.length - 50} more`);
  }
  return lines;
}

export function titleFor(event: GEvent, rule: RuleRow, source: CalendarRow, detail: Detail): string {
  if (detail === 'busy') {
    // Only the source label is available here; the title never leaks into a busy block.
    return renderTemplate(rule.busy_title, { source: source.label }) || 'Busy';
  }
  return (
    renderTemplate(rule.title_template, {
      source: source.label,
      title: event.summary?.trim() || '(No title)',
      organizer: event.organizer?.displayName ?? event.organizer?.email,
      location: event.location,
    }) || event.summary || 'Busy'
  );
}

export function descriptionFor(event: GEvent, rule: RuleRow, source: CalendarRow): string {
  const blocks: string[] = [];
  if (rule.include_description && event.description?.trim()) blocks.push(event.description.trim());
  const meta = [
    ...(rule.include_conference ? conferenceLines(event) : []),
    ...(rule.include_attendees ? attendeeLines(event) : []),
  ];
  if (meta.length) blocks.push(meta.join('\n'));
  blocks.push(`Cascaded from ${source.label}.`);
  return blocks.join('\n\n');
}

export interface BuiltMirror {
  kind: MirrorKind;
  payload: GEventInput;
}

function shift(iso: string, minutes: number): string {
  return new Date(new Date(iso).getTime() + minutes * 60_000).toISOString();
}

export function buildMirrors(
  event: GEvent,
  rule: RuleRow,
  source: CalendarRow,
  target: CalendarRow,
): BuiltMirror[] {
  const detail = effectiveDetail(rule, target, event);
  const privateProps = (kind: MirrorKind): Record<string, string> => ({
    [PROP.marker]: '1',
    [PROP.rule]: rule.id,
    [PROP.sourceCalendar]: source.id,
    [PROP.sourceEvent]: event.id,
    [PROP.kind]: kind,
  });
  const reminders: GEventInput['reminders'] = rule.keep_reminders
    ? { useDefault: true }
    : { useDefault: false, overrides: [] };

  const main: GEventInput = {
    summary: titleFor(event, rule, source, detail),
    start: { ...event.start },
    end: { ...event.end },
    transparency: rule.show_as === 'free' ? 'transparent' : 'opaque',
    visibility: rule.visibility,
    reminders,
    extendedProperties: { private: privateProps('main') },
  };
  if (rule.color_id) main.colorId = rule.color_id;
  if (detail === 'full') {
    main.description = descriptionFor(event, rule, source);
    if (rule.include_location && event.location) main.location = event.location;
  }

  const out: BuiltMirror[] = [{ kind: 'main', payload: main }];
  if (isAllDay(event) || !event.start?.dateTime || !event.end?.dateTime) return out;

  const tz = event.start.timeZone ?? target.time_zone ?? undefined;
  const buffer = (kind: MirrorKind, start: string, end: string): BuiltMirror => ({
    kind,
    payload: {
      summary: renderTemplate(rule.buffer_title, { source: source.label }) || 'Buffer',
      start: { dateTime: start, ...(tz ? { timeZone: tz } : {}) },
      end: { dateTime: end, ...(tz ? { timeZone: tz } : {}) },
      transparency: 'opaque',
      visibility: rule.visibility,
      reminders: { useDefault: false, overrides: [] },
      ...(rule.color_id ? { colorId: rule.color_id } : {}),
      extendedProperties: { private: privateProps(kind) },
    },
  });
  if (rule.buffer_before_min > 0) {
    const s = event.start.dateTime;
    out.push(buffer('buffer_before', shift(s, -rule.buffer_before_min), new Date(s).toISOString()));
  }
  if (rule.buffer_after_min > 0) {
    const e = event.end.dateTime;
    out.push(buffer('buffer_after', new Date(e).toISOString(), shift(e, rule.buffer_after_min)));
  }
  return out;
}
