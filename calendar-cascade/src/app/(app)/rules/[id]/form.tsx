'use client';

import { useMemo, useState } from 'react';
import { Submit } from '@/components/buttons';
import { buildMirrors, effectiveDetail, skipReason } from '@/lib/engine/mirror';
import { DETAIL_LABEL, type CalendarRow, type GEvent, type RuleRow } from '@/lib/engine/types';
import { saveRule } from '../../../actions';

const SAMPLE: GEvent = {
  id: 'sample',
  status: 'confirmed',
  summary: 'Roadmap review',
  description: 'Walk through Q4 priorities and the launch checklist.',
  location: 'HQ, Room 4',
  start: { dateTime: '2026-10-06T10:00:00-05:00', timeZone: 'America/Chicago' },
  end: { dateTime: '2026-10-06T11:00:00-05:00', timeZone: 'America/Chicago' },
  hangoutLink: 'https://meet.google.com/abc-defg-hij',
  organizer: { email: 'lead@example.com', displayName: 'Jordan Lee' },
  attendees: [
    { email: 'you@example.com', self: true, responseStatus: 'accepted' },
    { email: 'sam@example.com', displayName: 'Sam Rivera', responseStatus: 'accepted' },
  ],
};

const COLORS: [string, string][] = [
  ['', "Target calendar's colour"],
  ['1', 'Lavender'],
  ['2', 'Sage'],
  ['3', 'Grape'],
  ['4', 'Flamingo'],
  ['5', 'Banana'],
  ['6', 'Tangerine'],
  ['7', 'Peacock'],
  ['8', 'Graphite'],
  ['9', 'Blueberry'],
  ['10', 'Basil'],
  ['11', 'Tomato'],
];

function readForm(form: HTMLFormElement, base: RuleRow): RuleRow {
  const f = new FormData(form);
  const s = (k: string) => String(f.get(k) ?? '');
  const b = (k: string) => f.get(k) === 'on';
  const n = (k: string) => Math.max(0, Number(f.get(k)) || 0);
  return {
    ...base,
    enabled: b('enabled'),
    detail: s('detail') as RuleRow['detail'],
    title_template: s('title_template'),
    busy_title: s('busy_title'),
    include_description: b('include_description'),
    include_location: b('include_location'),
    include_attendees: b('include_attendees'),
    include_conference: b('include_conference'),
    visibility: s('visibility') as RuleRow['visibility'],
    show_as: s('show_as') as RuleRow['show_as'],
    color_id: s('color_id') || null,
    keep_reminders: b('keep_reminders'),
    buffer_before_min: n('buffer_before_min'),
    buffer_after_min: n('buffer_after_min'),
    buffer_title: s('buffer_title'),
    skip_all_day: b('skip_all_day'),
    skip_free: b('skip_free'),
    skip_declined: b('skip_declined'),
    skip_tentative: b('skip_tentative'),
    skip_if_native_on_target: b('skip_if_native_on_target'),
    exclude_keywords: s('exclude_keywords').split(',').map((x) => x.trim()).filter(Boolean),
    lookahead_days: n('lookahead_days') || 60,
  };
}

const fmt = (iso?: string) => (iso ? new Date(iso).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', timeZone: 'America/Chicago' }) : '');

export function RuleForm({ rule, source, target }: { rule: RuleRow; source: CalendarRow; target: CalendarRow }) {
  const [draft, setDraft] = useState(rule);
  const [privateSample, setPrivateSample] = useState(false);
  const sample = useMemo(() => ({ ...SAMPLE, visibility: privateSample ? ('private' as const) : undefined }), [privateSample]);
  const mirrors = useMemo(() => buildMirrors(sample, draft, source, target), [sample, draft, source, target]);
  const eff = effectiveDetail(draft, target, sample);
  const skip = skipReason(sample, draft);
  const full = draft.detail === 'full';

  return (
    <form action={saveRule} onChange={(e) => setDraft(readForm(e.currentTarget, rule))} style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.4fr) minmax(0, 1fr)', gap: 28, marginTop: 28, alignItems: 'start' }} className="rule-grid">
      <input type="hidden" name="id" value={rule.id} />
      <div className="stack" style={{ gap: 18 }}>
        <fieldset>
          <legend>Detail</legend>
          <label className="check">
            <input type="checkbox" name="enabled" defaultChecked={rule.enabled} />
            <span>Cascade {source.label} events to {target.label}</span>
          </label>
          <div className="fields">
            <label>
              Level
              <select name="detail" defaultValue={rule.detail}>
                <option value="full">Full context</option>
                <option value="title">Title only</option>
                <option value="busy">Busy block</option>
              </select>
            </label>
            <label>
              Title template
              <input type="text" name="title_template" defaultValue={rule.title_template} />
            </label>
            <label>
              Busy block title
              <input type="text" name="busy_title" defaultValue={rule.busy_title} />
            </label>
          </div>
          <p className="dim small">
            Tokens: <code>{'{{source}}'}</code> <code>{'{{title}}'}</code> <code>{'{{organizer}}'}</code> <code>{'{{location}}'}</code>. Busy titles only
            accept <code>{'{{source}}'}</code>.
            {target.inbound_max_detail !== 'full' && (
              <>
                {' '}
                {target.label}&apos;s ceiling is <b>{DETAIL_LABEL[target.inbound_max_detail].toLowerCase()}</b>; anything above that is capped.
              </>
            )}
          </p>
          <div className="fields" style={{ opacity: full ? 1 : 0.5 }}>
            <label className="check">
              <input type="checkbox" name="include_description" defaultChecked={rule.include_description} />
              <span>Description</span>
            </label>
            <label className="check">
              <input type="checkbox" name="include_location" defaultChecked={rule.include_location} />
              <span>Location</span>
            </label>
            <label className="check">
              <input type="checkbox" name="include_conference" defaultChecked={rule.include_conference} />
              <span>Join links and dial-in</span>
            </label>
            <label className="check">
              <input type="checkbox" name="include_attendees" defaultChecked={rule.include_attendees} />
              <span>
                Organizer and attendees
                <small>Listed in the description. Nobody is invited.</small>
              </span>
            </label>
          </div>
        </fieldset>

        <fieldset>
          <legend>Buffers</legend>
          <div className="fields">
            <label>
              Minutes before
              <input type="number" name="buffer_before_min" min={0} max={240} step={5} defaultValue={rule.buffer_before_min} />
            </label>
            <label>
              Minutes after
              <input type="number" name="buffer_after_min" min={0} max={240} step={5} defaultValue={rule.buffer_after_min} />
            </label>
            <label>
              Buffer title
              <input type="text" name="buffer_title" defaultValue={rule.buffer_title} />
            </label>
          </div>
          <p className="dim small">Buffers are separate busy events either side of timed events, so the mirror keeps its real times.</p>
        </fieldset>

        <fieldset>
          <legend>How it looks</legend>
          <div className="fields">
            <label>
              Show as
              <select name="show_as" defaultValue={rule.show_as}>
                <option value="busy">Busy</option>
                <option value="free">Free</option>
              </select>
            </label>
            <label>
              Visibility
              <select name="visibility" defaultValue={rule.visibility}>
                <option value="default">Calendar default</option>
                <option value="private">Private</option>
                <option value="public">Public</option>
              </select>
            </label>
            <label>
              Colour
              <select name="color_id" defaultValue={rule.color_id ?? ''}>
                {COLORS.map(([v, l]) => (
                  <option key={v} value={v}>
                    {l}
                  </option>
                ))}
              </select>
            </label>
          </div>
          <label className="check">
            <input type="checkbox" name="keep_reminders" defaultChecked={rule.keep_reminders} />
            <span>
              Keep {target.label}&apos;s default reminders
              <small>Off by default, so one meeting does not notify you four times.</small>
            </span>
          </label>
        </fieldset>

        <fieldset>
          <legend>Which events</legend>
          <div className="fields">
            <label className="check">
              <input type="checkbox" name="skip_all_day" defaultChecked={rule.skip_all_day} />
              <span>Skip all-day events</span>
            </label>
            <label className="check">
              <input type="checkbox" name="skip_free" defaultChecked={rule.skip_free} />
              <span>Skip events shown as free</span>
            </label>
            <label className="check">
              <input type="checkbox" name="skip_declined" defaultChecked={rule.skip_declined} />
              <span>Skip events I declined</span>
            </label>
            <label className="check">
              <input type="checkbox" name="skip_tentative" defaultChecked={rule.skip_tentative} />
              <span>Skip tentative or unanswered invites</span>
            </label>
            <label className="check">
              <input type="checkbox" name="skip_if_native_on_target" defaultChecked={rule.skip_if_native_on_target} />
              <span>
                Skip if already invited there
                <small>Same invitation on both calendars: no duplicate.</small>
              </span>
            </label>
          </div>
          <div className="fields">
            <label>
              Exclude keywords (comma separated)
              <input type="text" name="exclude_keywords" defaultValue={rule.exclude_keywords.join(', ')} />
            </label>
            <label>
              Look ahead (days)
              <input type="number" name="lookahead_days" min={1} max={365} defaultValue={rule.lookahead_days} />
            </label>
          </div>
        </fieldset>

        <div className="row">
          <Submit pendingText="Saving…">Save and sync</Submit>
          <span className="dim small">Existing mirrors are rewritten to match.</span>
        </div>
      </div>

      <aside className="stack" style={{ position: 'sticky', top: 24 }}>
        <span className="eyebrow">Preview on {target.label}</span>
        <div className="preview">
          {!draft.enabled ? (
            <p className="muted small">Off. Nothing is written.</p>
          ) : skip ? (
            <p className="muted small">This sample would be skipped: {skip}.</p>
          ) : (
            mirrors
              .slice()
              .sort((a, b) => new Date(a.payload.start.dateTime ?? 0).getTime() - new Date(b.payload.start.dateTime ?? 0).getTime())
              .map((m) => (
                <div key={m.kind} className={`ev ${m.kind === 'main' ? '' : 'buffer'}`}>
                  <b style={{ color: 'var(--ink-bright)' }}>{m.payload.summary}</b>
                  <div className="dim small mono">
                    {fmt(m.payload.start.dateTime)} to {fmt(m.payload.end.dateTime)} · {m.payload.transparency === 'opaque' ? 'busy' : 'free'}
                    {m.payload.location ? ` · ${m.payload.location}` : ''}
                  </div>
                  {m.payload.description && <pre>{m.payload.description}</pre>}
                </div>
              ))
          )}
        </div>
        <p className="dim small">
          Sample event &ldquo;{SAMPLE.summary}&rdquo; on {source.label}. Effective level: <b>{DETAIL_LABEL[eff].toLowerCase()}</b>.
        </p>
        <label className="check small">
          <input type="checkbox" checked={privateSample} onChange={(e) => setPrivateSample(e.target.checked)} />
          <span>Preview as a private event (always cascades as a busy block)</span>
        </label>
      </aside>
      <style>{`@media (max-width: 860px) { .rule-grid { grid-template-columns: 1fr !important; } }`}</style>
    </form>
  );
}
