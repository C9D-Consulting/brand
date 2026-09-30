import { ConfirmSubmit, Submit } from '@/components/buttons';
import { ago } from '@/components/format';
import { getAccounts, getCalendars, type AccountRow } from '@/lib/data';
import { DETAIL_LABEL, DETAILS, type CalendarRow, type Detail } from '@/lib/engine/types';
import { listCalendars, type CalendarListEntry } from '@/lib/google/calendar';
import { accessToken } from '@/lib/google/oauth';
import { webhooksAvailable } from '@/lib/sync/watch';
import { addCalendar, removeAccount, removeCalendar, updateCalendar } from '../../actions';

async function available(account: AccountRow): Promise<{ items: CalendarListEntry[]; error?: string }> {
  try {
    return { items: await listCalendars(await accessToken(account.id)) };
  } catch (err) {
    return { items: [], error: (err as Error).message };
  }
}

export default async function CalendarsPage({ searchParams }: { searchParams: Promise<{ error?: string; account?: string }> }) {
  const [{ error, account: justConnected }, accounts, calendars] = await Promise.all([searchParams, getAccounts(), getCalendars()]);
  const lists = await Promise.all(accounts.map(available));

  return (
    <>
      <span className="eyebrow">Calendars</span>
      <h1>Connect accounts, choose calendars.</h1>
      <p className="lede">
        Each calendar has a policy: how much it shares with others by default, and a privacy ceiling on what it will accept.
        Adding a calendar creates rules to and from every other calendar from those policies; fine-tune them on the Cascade page.
      </p>
      {error && <p className="notice err small" style={{ marginTop: 20 }}>{error}</p>}
      {!webhooksAvailable() && (
        <p className="notice small" style={{ marginTop: 20 }}>
          <code>APP_URL</code> is not https, so Google cannot push changes here. Calendars sync on demand and on the cron until deployed.
        </p>
      )}

      <section className="section">
        <div className="section-head">
          <div>
            <span className="eyebrow">Your calendars</span>
            <h2>{calendars.length ? `${calendars.length} in the cascade` : 'None yet'}</h2>
          </div>
        </div>
        <div className="stack">
          {calendars.map((c) => (
            <CalendarSettings key={c.id} cal={c} account={accounts.find((a) => a.id === c.account_id)} />
          ))}
          {!calendars.length && <p className="muted">Connect a Google account below, then add its calendars.</p>}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <span className="eyebrow">Google accounts</span>
            <h2>Where calendars come from</h2>
            <p className="muted small" style={{ marginTop: 6 }}>
              Connect one Google account per identity (employer, company, startup, personal). Tokens are encrypted at rest.
            </p>
          </div>
          <a className="button" href="/api/google/connect">
            Connect a Google account
          </a>
        </div>
        <div className="stack">
          {accounts.map((a, i) => (
            <div className="card" key={a.id} style={justConnected === a.id ? { borderColor: 'var(--stamp-dim)' } : undefined}>
              <div className="row" style={{ justifyContent: 'space-between' }}>
                <div className="row">
                  <h3>{a.email}</h3>
                  <span className={`pill ${a.status === 'active' ? 'ok' : 'err'}`}>{a.status === 'active' ? 'connected' : 'needs reconnect'}</span>
                  {justConnected === a.id && <span className="pill warn">just connected</span>}
                </div>
                <div className="row">
                  <a className="button ghost" href={`/api/google/connect?hint=${encodeURIComponent(a.email)}`}>
                    Reconnect
                  </a>
                  <form action={removeAccount}>
                    <input type="hidden" name="id" value={a.id} />
                    <ConfirmSubmit className="danger" message={`Disconnect ${a.email}? Its calendars leave the cascade and every mirror they wrote or received is deleted.`}>
                      Disconnect
                    </ConfirmSubmit>
                  </form>
                </div>
              </div>
              {lists[i].error && <p className="notice err small" style={{ marginTop: 12 }}>{lists[i].error}</p>}
              <AvailableCalendars account={a} items={lists[i].items} added={calendars} />
            </div>
          ))}
          {!accounts.length && <p className="muted">No accounts connected yet.</p>}
        </div>
      </section>
    </>
  );
}

function DetailSelect({ name, value }: { name: string; value: Detail }) {
  return (
    <select name={name} defaultValue={value}>
      {DETAILS.map((d) => (
        <option key={d} value={d}>
          {DETAIL_LABEL[d]}
        </option>
      ))}
    </select>
  );
}

function AvailableCalendars({ account, items, added }: { account: AccountRow; items: CalendarListEntry[]; added: CalendarRow[] }) {
  const taken = new Set(added.filter((c) => c.account_id === account.id).map((c) => c.google_calendar_id));
  const writable = items.filter((c) => (c.accessRole === 'owner' || c.accessRole === 'writer') && !taken.has(c.id));
  const readOnly = items.filter((c) => c.accessRole !== 'owner' && c.accessRole !== 'writer');
  if (!items.length) return null;
  return (
    <div className="stack" style={{ marginTop: 16 }}>
      {writable.map((c) => (
        <form key={c.id} action={addCalendar} className="card inset">
          <input type="hidden" name="account_id" value={account.id} />
          <input type="hidden" name="google_calendar_id" value={c.id} />
          <input type="hidden" name="time_zone" value={c.timeZone ?? ''} />
          <div className="row" style={{ justifyContent: 'space-between', marginBottom: 12 }}>
            <span className="row" style={{ gap: 8 }}>
              <span className="dot" style={{ background: c.backgroundColor ?? 'var(--stamp)' }} />
              <b>{c.summaryOverride ?? c.summary}</b>
              {c.primary && <span className="pill">primary</span>}
            </span>
            <span className="dim small mono">{c.id}</span>
          </div>
          <div className="fields">
            <label>
              Label (used as the prefix)
              <input type="text" name="label" defaultValue={c.primary ? '' : (c.summaryOverride ?? c.summary)} placeholder="e.g. Sayer" required />
            </label>
            <label>
              Shares with others
              <DetailSelect name="outbound_detail" value="full" />
            </label>
            <label>
              Privacy ceiling (accepts at most)
              <DetailSelect name="inbound_max_detail" value="full" />
            </label>
            <label>
              Colour
              <input type="color" name="color" defaultValue={c.backgroundColor ?? '#d6743a'} />
            </label>
          </div>
          <div className="row" style={{ marginTop: 14 }}>
            <Submit pendingText="Adding…">Add to cascade</Submit>
            <span className="dim small">Tip: for an employer calendar, set the ceiling to Busy block.</span>
          </div>
        </form>
      ))}
      {!writable.length && <p className="dim small">Every writable calendar on this account is already in the cascade.</p>}
      {readOnly.length > 0 && (
        <p className="dim small">
          {readOnly.length} read-only calendar{readOnly.length === 1 ? '' : 's'} hidden: the cascade needs write access to keep a calendar blocked.
        </p>
      )}
    </div>
  );
}

function CalendarSettings({ cal, account }: { cal: CalendarRow; account?: AccountRow }) {
  const watching = cal.watch_expires_at && new Date(cal.watch_expires_at) > new Date();
  return (
    <div className="card">
      <form action={updateCalendar}>
        <input type="hidden" name="id" value={cal.id} />
        <div className="row" style={{ justifyContent: 'space-between', marginBottom: 14 }}>
          <span className="row" style={{ gap: 10 }}>
            <span className="dot" style={{ background: cal.color, width: 12, height: 12 }} />
            <h3>{cal.label}</h3>
            <span className="dim small">{account?.email}</span>
          </span>
          <span className="row small" style={{ gap: 8 }}>
            {watching ? <span className="pill ok" title="Google pushes changes here; the channel renews automatically">live · expires {ago(cal.watch_expires_at)}</span> : <span className="pill warn">polling</span>}
            <span className="dim">synced {ago(cal.last_synced_at)}</span>
          </span>
        </div>
        {cal.last_sync_error && <p className="notice err small" style={{ marginBottom: 14 }}>{cal.last_sync_error}</p>}
        <div className="fields">
          <label>
            Label
            <input type="text" name="label" defaultValue={cal.label} required />
          </label>
          <label>
            Shares with others
            <DetailSelect name="outbound_detail" value={cal.outbound_detail} />
          </label>
          <label>
            Privacy ceiling
            <DetailSelect name="inbound_max_detail" value={cal.inbound_max_detail} />
          </label>
          <label>
            Order
            <input type="number" name="sort_order" defaultValue={cal.sort_order} min={0} max={999} />
          </label>
          <label>
            Colour
            <input type="color" name="color" defaultValue={cal.color} />
          </label>
        </div>
        <div className="row" style={{ marginTop: 14, justifyContent: 'space-between' }}>
          <label className="check">
            <input type="checkbox" name="enabled" defaultChecked={cal.enabled} />
            <span>
              In the cascade
              <small>Paused calendars neither send nor receive; their mirrors are removed.</small>
            </span>
          </label>
          <Submit pendingText="Saving…">Save</Submit>
        </div>
      </form>
      <details style={{ marginTop: 12 }}>
        <summary className="small">Remove from cascade</summary>
        <form action={removeCalendar} className="row" style={{ marginTop: 10 }}>
          <input type="hidden" name="id" value={cal.id} />
          <label className="check">
            <input type="checkbox" name="purge" defaultChecked />
            <span>Also delete every mirror it sent and received</span>
          </label>
          <ConfirmSubmit className="danger" message={`Remove ${cal.label} from the cascade?`}>
            Remove {cal.label}
          </ConfirmSubmit>
        </form>
      </details>
    </div>
  );
}
