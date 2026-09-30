import type { GEvent, GEventInput } from '@/lib/engine/types';

// An in-memory Google Calendar: calendarId -> eventId -> event.
export class FakeGoogle {
  calendars = new Map<string, Map<string, GEvent>>();
  writes = 0;
  private seq = 0;

  cal(id: string) {
    if (!this.calendars.has(id)) this.calendars.set(id, new Map());
    return this.calendars.get(id)!;
  }

  add(calendarId: string, event: GEvent) {
    this.cal(calendarId).set(event.id, event);
  }

  events(calendarId: string) {
    return [...this.cal(calendarId).values()];
  }

  api = {
    listEvents: async (_t: string, calendarId: string, min: Date, max: Date) =>
      this.events(calendarId).filter((e) => {
        const s = new Date(e.start!.dateTime ?? `${e.start!.date}T00:00:00Z`);
        const en = new Date(e.end!.dateTime ?? `${e.end!.date}T00:00:00Z`);
        return en > min && s < max && e.status !== 'cancelled';
      }),
    insertEvent: async (_t: string, calendarId: string, body: GEventInput) => {
      this.writes++;
      const ev = { ...(body as unknown as GEvent), id: `g${++this.seq}`, iCalUID: `g${this.seq}@google.com` };
      this.add(calendarId, ev);
      return ev;
    },
    updateEvent: async (_t: string, calendarId: string, id: string, body: GEventInput) => {
      this.writes++;
      const prev = this.cal(calendarId).get(id);
      if (!prev) {
        const { GoogleApiError } = await import('@/lib/google/calendar');
        throw new GoogleApiError(404, 'not found');
      }
      const ev = { ...(body as unknown as GEvent), id, iCalUID: prev.iCalUID };
      this.add(calendarId, ev);
      return ev;
    },
    deleteEvent: async (_t: string, calendarId: string, id: string) => {
      this.writes++;
      this.cal(calendarId).delete(id);
    },
  };
}
