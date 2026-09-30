// Desired state for one source calendar, and the diff against what exists.

import { hashPayload } from './hash';
import { buildMirrors, eventRange, skipReason } from './mirror';
import type { CalendarRow, GEvent, GEventInput, MirrorKind, MirrorRow, RuleRow } from './types';

export interface DesiredMirror {
  key: string;
  ruleId: string;
  sourceEventId: string;
  targetCalendarId: string;
  kind: MirrorKind;
  sourceStart: string;
  sourceEnd: string;
  payload: GEventInput;
  hash: string;
}

export interface PlanInput {
  source: CalendarRow;
  rules: RuleRow[]; // active rules for this source only
  calendars: Map<string, CalendarRow>;
  events: GEvent[];
  now: Date;
  nativeICalUIDs?: Map<string, Set<string>>; // by target calendar id
}

export interface PlanOutput {
  desired: DesiredMirror[];
  skipped: { eventId: string; ruleId: string; reason: string }[];
}

export const mirrorKey = (ruleId: string, sourceEventId: string, kind: MirrorKind) =>
  `${ruleId}:${sourceEventId}:${kind}`;

export function planSource(input: PlanInput): PlanOutput {
  const desired: DesiredMirror[] = [];
  const skipped: PlanOutput['skipped'] = [];
  for (const rule of input.rules) {
    const target = input.calendars.get(rule.target_calendar_id);
    if (!target) continue;
    const horizon = new Date(input.now.getTime() + rule.lookahead_days * 86_400_000);
    for (const event of input.events) {
      const reason = skipReason(event, rule, {
        horizon,
        nativeICalUIDs: input.nativeICalUIDs?.get(target.id),
      });
      if (reason) {
        skipped.push({ eventId: event.id, ruleId: rule.id, reason });
        continue;
      }
      const range = eventRange(event)!;
      for (const built of buildMirrors(event, rule, input.source, target)) {
        desired.push({
          key: mirrorKey(rule.id, event.id, built.kind),
          ruleId: rule.id,
          sourceEventId: event.id,
          targetCalendarId: target.id,
          kind: built.kind,
          sourceStart: range.start.toISOString(),
          sourceEnd: range.end.toISOString(),
          payload: built.payload,
          hash: hashPayload(built.payload),
        });
      }
    }
  }
  return { desired, skipped };
}

export type Op =
  | { type: 'create'; want: DesiredMirror }
  | { type: 'update'; want: DesiredMirror; have: MirrorRow }
  | { type: 'recreate'; want: DesiredMirror; have: MirrorRow }
  | { type: 'delete'; have: MirrorRow };

export interface DiffInput {
  desired: DesiredMirror[];
  existing: MirrorRow[];
  // Source event ids returned by the listing that produced `desired`.
  listedSourceEventIds: Set<string>;
  // Start of the listing window. Mirrors whose source ended before it were not
  // looked at and must be left alone.
  windowStart: Date;
  // Target event ids actually present, by target calendar id. When a target was
  // listed, a mirror missing from it was deleted by hand and gets recreated.
  presentOnTarget?: Map<string, Set<string>>;
}

export function diff(input: DiffInput): Op[] {
  const ops: Op[] = [];
  const have = new Map(input.existing.map((m) => [mirrorKey(m.rule_id, m.source_event_id, m.kind), m]));
  const wanted = new Set<string>();
  for (const want of input.desired) {
    wanted.add(want.key);
    const row = have.get(want.key);
    if (!row) {
      ops.push({ type: 'create', want });
      continue;
    }
    const present = input.presentOnTarget?.get(row.target_calendar_id);
    if (present && !present.has(row.target_event_id)) {
      ops.push({ type: 'recreate', want, have: row });
    } else if (row.content_hash !== want.hash) {
      ops.push({ type: 'update', want, have: row });
    }
  }
  for (const [key, row] of have) {
    if (wanted.has(key)) continue;
    const inWindow = new Date(row.source_end) > input.windowStart;
    if (input.listedSourceEventIds.has(row.source_event_id) || inWindow) {
      ops.push({ type: 'delete', have: row });
    }
  }
  return ops;
}
