import { beforeEach, describe, expect, it, vi } from 'vitest';
import { FakeDb } from './fakes/db';
import { FakeGoogle } from './fakes/google';
import { all, event, rule } from './fixtures';

const fake = vi.hoisted(() => ({ db: null as any, google: null as any }));

vi.mock('@/lib/supabase', () => ({
  db: () => fake.db,
  must: (res: { data: unknown; error: { message: string } | null }) => {
    if (res.error) throw new Error(res.error.message);
    return res.data;
  },
}));
vi.mock('@/lib/google/oauth', () => ({ accessToken: async () => 'token' }));
vi.mock('@/lib/google/calendar', async (orig) => {
  const real = await orig<typeof import('@/lib/google/calendar')>();
  return {
    ...real,
    listEvents: (...a: any[]) => fake.google.api.listEvents(...a),
    insertEvent: (...a: any[]) => fake.google.api.insertEvent(...a),
    updateEvent: (...a: any[]) => fake.google.api.updateEvent(...a),
    deleteEvent: (...a: any[]) => fake.google.api.deleteEvent(...a),
  };
});

const { reconcileSource } = await import('@/lib/sync/reconcile');

const now = new Date('2026-09-30T12:00:00Z');
const g = (calId: string) => `${calId}@example.com`;

let db: FakeDb;
let google: FakeGoogle;

beforeEach(() => {
  db = new FakeDb();
  google = new FakeGoogle();
  fake.db = db;
  fake.google = google;
  db.tables.calendars = all.map((c) => ({ ...c }));
  db.tables.rules = all.flatMap((s) => all.filter((t) => t.id !== s.id).map((t) => rule(s, t)));
});

async function syncEverything() {
  for (const c of all) await reconcileSource(c.id, now);
}

describe('reconcileSource', () => {
  it('cascades a Sayer meeting with context everywhere, and C9D work as a bare block to Sayer', async () => {
    google.add(g('sayer'), event({ id: 's1', summary: 'Standup' }));
    google.add(g('c9d'), event({ id: 'c1', summary: 'Client kickoff', iCalUID: 'c1@google.com' }));
    await syncEverything();

    const titles = (id: string) => google.events(g(id)).map((e) => e.summary).sort();
    expect(titles('sayer')).toEqual(['Block', 'Standup']);
    expect(titles('c9d')).toEqual(['Client kickoff', 'Sayer: Standup']);
    expect(titles('mk')).toEqual(['C9D Consulting: Client kickoff', 'Sayer: Standup']);
    expect(titles('pro')).toEqual(['C9D Consulting: Client kickoff', 'Sayer: Standup']);
    const block = google.events(g('sayer')).find((e) => e.summary === 'Block')!;
    expect(block.description).toBeUndefined();
    expect(db.tables.mirrors).toHaveLength(6);
  });

  it('never loops: a second full pass writes nothing', async () => {
    google.add(g('sayer'), event({ id: 's1' }));
    google.add(g('mk'), event({ id: 'm1', iCalUID: 'm1@google.com' }));
    await syncEverything();
    const writes = google.writes;
    await syncEverything();
    await syncEverything();
    expect(google.writes).toBe(writes);
  });

  it('propagates edits and deletions', async () => {
    google.add(g('sayer'), event({ id: 's1', summary: 'Standup' }));
    await syncEverything();

    google.add(g('sayer'), event({ id: 's1', summary: 'Standup (moved)', start: { dateTime: '2026-10-01T13:00:00-05:00' }, end: { dateTime: '2026-10-01T14:00:00-05:00' } }));
    await reconcileSource('sayer', now);
    expect(google.events(g('pro')).map((e) => e.summary)).toEqual(['Sayer: Standup (moved)']);
    expect(google.events(g('pro'))[0].start?.dateTime).toBe('2026-10-01T13:00:00-05:00');

    google.cal(g('sayer')).delete('s1');
    await reconcileSource('sayer', now);
    for (const id of ['c9d', 'mk', 'pro']) expect(google.events(g(id))).toEqual([]);
    expect(db.tables.mirrors).toHaveLength(0);
  });

  it('puts back a mirror someone deleted by hand', async () => {
    google.add(g('sayer'), event({ id: 's1' }));
    await syncEverything();
    const [mirror] = google.events(g('mk'));
    google.cal(g('mk')).delete(mirror.id);
    await reconcileSource('sayer', now);
    expect(google.events(g('mk'))).toHaveLength(1);
  });

  it('turning a rule off removes its mirrors; tightening a ceiling strips details', async () => {
    google.add(g('sayer'), event({ id: 's1', summary: 'Standup' }));
    await syncEverything();

    db.tables.rules.find((r) => r.id === 'sayer->mk')!.enabled = false;
    db.tables.calendars.find((c) => c.id === 'pro')!.inbound_max_detail = 'busy';
    await reconcileSource('sayer', now);

    expect(google.events(g('mk'))).toEqual([]);
    const [onPro] = google.events(g('pro'));
    expect(onPro.summary).toBe('Block');
    expect(onPro.description).toBeUndefined();
  });

  it('writes buffers either side and cleans them up with the event', async () => {
    db.tables.rules.find((r) => r.id === 'c9d->sayer')!.buffer_before_min = 15;
    db.tables.rules.find((r) => r.id === 'c9d->sayer')!.buffer_after_min = 15;
    google.add(g('c9d'), event({ id: 'c1' }));
    await reconcileSource('c9d', now);
    expect(google.events(g('sayer')).map((e) => e.summary).sort()).toEqual(['Block', 'Buffer', 'Buffer']);

    google.cal(g('c9d')).delete('c1');
    await reconcileSource('c9d', now);
    expect(google.events(g('sayer'))).toEqual([]);
  });

  it('does not duplicate an invitation that is already on the target', async () => {
    google.add(g('sayer'), event({ id: 's1', iCalUID: 'shared@google.com' }));
    google.add(g('c9d'), event({ id: 'c-native', iCalUID: 'shared@google.com' }));
    await reconcileSource('sayer', now);
    expect(google.events(g('c9d'))).toHaveLength(1);
    expect(google.events(g('mk'))).toHaveLength(1);
  });

  it('removes stray events left by an interrupted run', async () => {
    google.add(g('sayer'), event({ id: 's1' }));
    await reconcileSource('sayer', now);
    // Simulate a crash after the Google write but before the mirror row was saved.
    db.tables.mirrors = db.tables.mirrors.filter((m) => m.target_calendar_id !== 'mk');
    await reconcileSource('sayer', now);
    expect(google.events(g('mk'))).toHaveLength(1);
  });
});
