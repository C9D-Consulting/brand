import Link from 'next/link';
import { AutoSelect, ConfirmSubmit, Submit } from '@/components/buttons';
import { ago } from '@/components/format';
import { ActivityList } from '@/components/activity';
import { countMirrors, getAccounts, getActivity, getCalendars, getRules } from '@/lib/data';
import { effectiveDetail } from '@/lib/engine/mirror';
import { describeRule } from '@/lib/engine/policy';
import { DETAIL_LABEL, type CalendarRow, type RuleRow } from '@/lib/engine/types';
import { resetMatrix, setRuleDetail, syncNow } from '../actions';

export default async function CascadePage({ searchParams }: { searchParams: Promise<{ saved?: string }> }) {
  const [calendars, rules, accounts, activity, counts, { saved }] = await Promise.all([
    getCalendars(),
    getRules(),
    getAccounts(),
    getActivity(8),
    countMirrors(),
    searchParams,
  ]);

  if (!calendars.length) {
    return (
      <>
        <span className="eyebrow">Get started</span>
        <h1>Keep every calendar blocked.</h1>
        <p className="lede">
          Connect each Google account, add the calendars you want kept in step, and Calendar Cascade writes a mirror of every
          event onto the others: full context where you want it, a bare block where you do not, with buffers either side.
        </p>
        <div className="row" style={{ marginTop: 24 }}>
          <Link className="button" href="/calendars">
            Connect a calendar
          </Link>
        </div>
      </>
    );
  }

  const rule = new Map(rules.map((r) => [`${r.source_calendar_id}>${r.target_calendar_id}`, r]));
  const brokenAccounts = accounts.filter((a) => a.status === 'error');
  const total = Object.values(counts).reduce((a, b) => a + b, 0);

  return (
    <>
      {saved && <p className="notice small" style={{ marginBottom: 24 }}>Rule saved. Syncing in the background.</p>}
      {brokenAccounts.map((a) => (
        <p key={a.id} className="notice err small" style={{ marginBottom: 12 }}>
          {a.email}: {a.last_error ?? 'access failed'} <a href={`/api/google/connect?hint=${encodeURIComponent(a.email)}`}>Reconnect</a>
        </p>
      ))}

      <div className="section-head">
        <div>
          <span className="eyebrow">The cascade</span>
          <h1>Where each event goes.</h1>
          <p className="lede">
            Rows are where an event starts; columns are where its mirror lands. Change a cell and that calendar resyncs.
            A calendar&apos;s privacy ceiling always wins, so an employer calendar set to <em>busy</em> never receives details.
          </p>
        </div>
        <div className="row">
          <form action={resetMatrix}>
            <ConfirmSubmit className="ghost" message="Reset every cell to what the calendar policies say? Templates, buffers and filters are kept.">
              Reset from policies
            </ConfirmSubmit>
          </form>
          <form action={syncNow}>
            <Submit pendingText="Syncing…">Sync everything</Submit>
          </form>
        </div>
      </div>

      <div className="matrix-wrap">
        <table className="matrix">
          <thead>
            <tr>
              <th className="corner">From ↓ &nbsp; To →</th>
              {calendars.map((t) => (
                <th key={t.id}>
                  <span className="row" style={{ gap: 8 }}>
                    <span className="dot" style={{ background: t.color }} />
                    {t.label}
                  </span>
                  <span className="dim small">ceiling: {DETAIL_LABEL[t.inbound_max_detail].toLowerCase()}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {calendars.map((s) => (
              <tr key={s.id}>
                <th>
                  <span className="row" style={{ gap: 8 }}>
                    <span className="dot" style={{ background: s.color }} />
                    {s.label}
                  </span>
                  {!s.enabled && <span className="pill warn">paused</span>}
                </th>
                {calendars.map((t) =>
                  s.id === t.id ? (
                    <td key={t.id} className="self" aria-label="same calendar" />
                  ) : (
                    <MatrixCell key={t.id} rule={rule.get(`${s.id}>${t.id}`)} target={t} count={counts[rule.get(`${s.id}>${t.id}`)?.id ?? ''] ?? 0} />
                  ),
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="dim small" style={{ marginTop: 10 }}>
        {total} upcoming mirrored events across {calendars.length} calendars. Add <code>#nocascade</code> to any event to keep it where it is.
      </p>

      <section className="section">
        <span className="eyebrow">In plain English</span>
        <div className="grid">
          {calendars.map((s) => (
            <div className="card" key={s.id}>
              <div className="row" style={{ justifyContent: 'space-between' }}>
                <h3 className="row" style={{ gap: 8, flexWrap: 'nowrap', alignItems: 'baseline' }}>
                  <span className="dot" style={{ background: s.color, transform: 'translateY(-1px)' }} />
                  When {s.label} gets an event
                </h3>
              </div>
              <ul className="flow small" style={{ paddingLeft: 18, marginTop: 10 }}>
                {calendars
                  .filter((t) => t.id !== s.id)
                  .map((t) => {
                    const r = rule.get(`${s.id}>${t.id}`);
                    return <li key={t.id}>{r ? describeRule(r, s, t) : `${t.label}: no rule yet.`}</li>;
                  })}
              </ul>
              <CalendarStatus cal={s} />
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <span className="eyebrow">Recent activity</span>
          <Link className="small" href="/activity">
            All activity
          </Link>
        </div>
        <ActivityList rows={activity} calendars={calendars} />
      </section>
    </>
  );
}

function MatrixCell({ rule, target, count }: { rule?: RuleRow; target: CalendarRow; count: number }) {
  if (!rule) return <td className="dim small">Syncing rules…</td>;
  const eff = effectiveDetail(rule, target);
  const value = rule.enabled ? rule.detail : 'off';
  return (
    <td>
      <div className={`cell ${rule.enabled ? '' : 'off'}`}>
        <form action={setRuleDetail}>
          <input type="hidden" name="id" value={rule.id} />
          <AutoSelect name="value" defaultValue={value} key={value} aria-label={`Detail sent to ${target.label}`}>
            <option value="full">Full context</option>
            <option value="title">Title only</option>
            <option value="busy">Busy block</option>
            <option value="off">Off</option>
          </AutoSelect>
        </form>
        <div className="meta">
          {rule.enabled && eff !== rule.detail && <span className="pill warn">capped: {eff}</span>}
          {rule.enabled && (rule.buffer_before_min > 0 || rule.buffer_after_min > 0) && (
            <span title="Buffers before / after">
              ⧗ {rule.buffer_before_min}/{rule.buffer_after_min}m
            </span>
          )}
          {rule.enabled && <span title="Upcoming mirrors">{count} live</span>}
          <Link href={`/rules/${rule.id}`}>Customize</Link>
        </div>
      </div>
    </td>
  );
}

function CalendarStatus({ cal }: { cal: CalendarRow }) {
  const watching = cal.watch_expires_at && new Date(cal.watch_expires_at) > new Date();
  return (
    <div className="row small" style={{ marginTop: 14, justifyContent: 'space-between' }}>
      <span className="row" style={{ gap: 8 }}>
        {cal.last_sync_error ? (
          <span className="pill err" title={cal.last_sync_error}>
            error
          </span>
        ) : watching ? (
          <span className="pill ok" title={`Push channel until ${cal.watch_expires_at}`}>
            live
          </span>
        ) : (
          <span className="pill warn" title="No push channel: syncs on schedule or on demand">
            polling
          </span>
        )}
        <span className="dim">synced {ago(cal.last_synced_at)}</span>
      </span>
      <form action={syncNow}>
        <input type="hidden" name="id" value={cal.id} />
        <Submit className="link" pendingText="Syncing…">
          Sync now
        </Submit>
      </form>
    </div>
  );
}
