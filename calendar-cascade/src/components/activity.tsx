import { ago } from './format';
import type { ActivityRow } from '@/lib/data';
import type { CalendarRow } from '@/lib/engine/types';

export function ActivityList({ rows, calendars }: { rows: ActivityRow[]; calendars: CalendarRow[] }) {
  const byId = new Map(calendars.map((c) => [c.id, c]));
  if (!rows.length) return <p className="muted small">Nothing yet.</p>;
  return (
    <table className="table">
      <tbody>
        {rows.map((a) => (
          <tr key={a.id}>
            <td className="dim small mono" style={{ width: 110, whiteSpace: 'nowrap' }}>
              {ago(a.created_at)}
            </td>
            <td style={{ width: 90 }}>
              <span className={`pill ${a.level === 'error' ? 'err' : a.level === 'warn' ? 'warn' : ''}`}>{a.action}</span>
            </td>
            <td>
              {a.calendar_id && byId.get(a.calendar_id) && (
                <span className="dot" style={{ background: byId.get(a.calendar_id)!.color, marginRight: 8 }} />
              )}
              {a.message}
              {a.details && (
                <details className="small" style={{ marginTop: 4 }}>
                  <summary>details</summary>
                  <pre className="mono dim" style={{ whiteSpace: 'pre-wrap' }}>
                    {JSON.stringify(a.details, null, 2)}
                  </pre>
                </details>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
