import { describe, expect, it } from 'vitest';
import { buildMirrors, effectiveDetail, isManaged, skipReason } from '@/lib/engine/mirror';
import { diff, mirrorKey, planSource } from '@/lib/engine/plan';
import { describeRule } from '@/lib/engine/policy';
import { renderTemplate } from '@/lib/engine/template';
import type { MirrorRow } from '@/lib/engine/types';
import { all, c9d, calendarMap, event, mk, pro, rule, sayer } from './fixtures';

const now = new Date('2026-09-30T12:00:00Z');

function rulesFrom(sourceId: string) {
  const source = calendarMap.get(sourceId)!;
  return all.filter((c) => c.id !== sourceId).map((t) => rule(source, t));
}

describe('the brief', () => {
  it('Sayer events land on every other calendar with full context and a "Sayer:" prefix', () => {
    const { desired } = planSource({ source: sayer, rules: rulesFrom('sayer'), calendars: calendarMap, events: [event()], now });
    expect(desired.map((d) => d.targetCalendarId).sort()).toEqual(['c9d', 'mk', 'pro']);
    for (const d of desired) {
      expect(d.payload.summary).toBe('Sayer: Quarterly planning');
      expect(d.payload.description).toContain('Agenda: roadmap');
      expect(d.payload.description).toContain('Join: https://meet.google.com/abc-defg-hij');
      expect(d.payload.description).toContain('peer@sayer.com');
      expect(d.payload.location).toBe('Room 4');
      expect(d.payload.transparency).toBe('opaque');
    }
  });

  it.each([
    ['c9d', 'C9D Consulting'],
    ['mk', 'MonetizeKit'],
    ['pro', 'Brandon.Wilburn.Pro'],
  ])('%s events become a bare "Block" on Sayer and full context elsewhere', (id, label) => {
    const source = calendarMap.get(id)!;
    const { desired } = planSource({ source, rules: rulesFrom(id), calendars: calendarMap, events: [event()], now });
    const onSayer = desired.find((d) => d.targetCalendarId === 'sayer')!;
    expect(onSayer.payload.summary).toBe('Block');
    expect(onSayer.payload.description).toBeUndefined();
    expect(onSayer.payload.location).toBeUndefined();
    const others = desired.filter((d) => d.targetCalendarId !== 'sayer');
    expect(others).toHaveLength(2);
    for (const d of others) {
      expect(d.payload.summary).toBe(`${label}: Quarterly planning`);
      expect(d.payload.description).toContain('Agenda: roadmap');
    }
  });
});

describe('privacy', () => {
  it('the target ceiling caps a rule even if it asks for full', () => {
    expect(effectiveDetail({ detail: 'full' }, sayer)).toBe('busy');
    expect(describeRule(rule(c9d, sayer, { detail: 'full' }), c9d, sayer)).toContain('capped');
  });

  it('a private source event is only ever a busy block', () => {
    const [main] = buildMirrors(event({ visibility: 'private' }), rule(sayer, c9d), sayer, c9d);
    expect(main.payload.summary).toBe('Block');
    expect(main.payload.description).toBeUndefined();
  });

  it('a busy title template cannot pull in the event title', () => {
    const [main] = buildMirrors(event(), rule(c9d, sayer, { busy_title: '{{source}} {{title}}' }), c9d, sayer);
    expect(main.payload.summary).toBe('C9D Consulting');
  });

  it('title-only mode drops description, location and attendees', () => {
    const [main] = buildMirrors(event(), rule(c9d, mk, { detail: 'title' }), c9d, mk);
    expect(main.payload.summary).toBe('C9D Consulting: Quarterly planning');
    expect(main.payload.description).toBeUndefined();
    expect(main.payload.location).toBeUndefined();
  });

  it('mirrors never carry attendees, so no invitations are sent', () => {
    const [main] = buildMirrors(event(), rule(sayer, c9d), sayer, c9d);
    expect('attendees' in main.payload).toBe(false);
  });
});

describe('loops and filters', () => {
  it('events we wrote are never cascaded again', () => {
    const [main] = buildMirrors(event(), rule(sayer, c9d), sayer, c9d);
    const written = event({ id: 'mirror', extendedProperties: main.payload.extendedProperties });
    expect(isManaged(written)).toBe(true);
    expect(skipReason(written, rule(c9d, mk))).toBe('written by Calendar Cascade');
  });

  it.each([
    [{ status: 'cancelled' as const }, 'cancelled'],
    [{ transparency: 'transparent' as const }, 'shown as free'],
    [{ start: { date: '2026-10-01' }, end: { date: '2026-10-02' } }, 'all-day event'],
    [{ attendees: [{ self: true, responseStatus: 'declined' as const }] }, 'declined'],
    [{ summary: 'Dentist #nocascade' }, 'matches exclude keyword "#nocascade"'],
    [{ eventType: 'workingLocation' }, 'workingLocation event'],
  ])('skips %o', (over, reason) => {
    expect(skipReason(event(over), rule(sayer, c9d))).toBe(reason);
  });

  it('skips events already on the target via the same invitation', () => {
    const native = new Set(['evt1@google.com']);
    expect(skipReason(event(), rule(sayer, c9d), { nativeICalUIDs: native })).toBe('already on target calendar');
    expect(skipReason(event(), rule(sayer, c9d, { skip_if_native_on_target: false }), { nativeICalUIDs: native })).toBeNull();
  });

  it('respects the lookahead horizon', () => {
    const far = event({ start: { dateTime: '2027-06-01T10:00:00Z' }, end: { dateTime: '2027-06-01T11:00:00Z' } });
    const { desired, skipped } = planSource({ source: sayer, rules: [rule(sayer, c9d)], calendars: calendarMap, events: [far], now });
    expect(desired).toHaveLength(0);
    expect(skipped[0].reason).toBe('beyond lookahead');
  });
});

describe('buffers', () => {
  it('adds busy buffers before and after timed events', () => {
    const built = buildMirrors(event(), rule(sayer, c9d, { buffer_before_min: 15, buffer_after_min: 10 }), sayer, c9d);
    const before = built.find((b) => b.kind === 'buffer_before')!;
    const after = built.find((b) => b.kind === 'buffer_after')!;
    expect(before.payload.start.dateTime).toBe('2026-10-01T14:45:00.000Z');
    expect(before.payload.end.dateTime).toBe('2026-10-01T15:00:00.000Z');
    expect(after.payload.start.dateTime).toBe('2026-10-01T16:00:00.000Z');
    expect(after.payload.end.dateTime).toBe('2026-10-01T16:10:00.000Z');
    expect(before.payload.summary).toBe('Buffer');
    expect(before.payload.description).toBeUndefined();
  });

  it('never buffers all-day events', () => {
    const allDay = event({ start: { date: '2026-10-01' }, end: { date: '2026-10-02' } });
    const built = buildMirrors(allDay, rule(sayer, c9d, { buffer_before_min: 15, skip_all_day: false }), sayer, c9d);
    expect(built.map((b) => b.kind)).toEqual(['main']);
  });
});

describe('diff', () => {
  const r = rule(sayer, c9d);
  const plan = () => planSource({ source: sayer, rules: [r], calendars: calendarMap, events: [event()], now });
  const row = (over: Partial<MirrorRow> = {}): MirrorRow => ({
    id: 'm1',
    rule_id: r.id,
    source_calendar_id: 'sayer',
    source_event_id: 'evt1',
    target_calendar_id: 'c9d',
    target_event_id: 't1',
    kind: 'main',
    source_start: '2026-10-01T15:00:00.000Z',
    source_end: '2026-10-01T16:00:00.000Z',
    content_hash: plan().desired[0].hash,
    ...over,
  });
  const windowStart = new Date('2026-09-29T00:00:00Z');

  it('creates what is missing and leaves what matches', () => {
    const { desired } = plan();
    expect(diff({ desired, existing: [], listedSourceEventIds: new Set(['evt1']), windowStart })).toEqual([
      { type: 'create', want: desired[0] },
    ]);
    expect(diff({ desired, existing: [row()], listedSourceEventIds: new Set(['evt1']), windowStart })).toEqual([]);
  });

  it('updates when the content changed', () => {
    const ops = diff({ desired: plan().desired, existing: [row({ content_hash: 'stale' })], listedSourceEventIds: new Set(['evt1']), windowStart });
    expect(ops.map((o) => o.type)).toEqual(['update']);
  });

  it('recreates a mirror someone deleted from the target by hand', () => {
    const ops = diff({
      desired: plan().desired,
      existing: [row()],
      listedSourceEventIds: new Set(['evt1']),
      windowStart,
      presentOnTarget: new Map([['c9d', new Set<string>()]]),
    });
    expect(ops.map((o) => o.type)).toEqual(['recreate']);
  });

  it('deletes mirrors whose source event is gone, but not history outside the window', () => {
    const gone = row({ source_event_id: 'gone', id: 'm2' });
    const old = row({ source_event_id: 'old', id: 'm3', source_start: '2026-09-01T10:00:00Z', source_end: '2026-09-01T11:00:00Z' });
    const ops = diff({ desired: [], existing: [gone, old], listedSourceEventIds: new Set(), windowStart });
    expect(ops).toEqual([{ type: 'delete', have: gone }]);
  });

  it('keys mirrors by rule, source event and kind', () => {
    expect(mirrorKey('r', 'e', 'buffer_after')).toBe('r:e:buffer_after');
  });
});

describe('templates', () => {
  it('fills tokens and tidies the seams of empty ones', () => {
    expect(renderTemplate('{{source}}: {{title}}', { source: 'Sayer', title: 'Standup' })).toBe('Sayer: Standup');
    expect(renderTemplate('{{title}} ({{location}})', { title: 'Lunch' })).toBe('Lunch');
    expect(renderTemplate('{{source}}: {{title}}', { source: 'Sayer' })).toBe('Sayer');
  });
});
