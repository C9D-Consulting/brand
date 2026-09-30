import 'server-only';
import type { GEvent, GEventInput } from '../engine/types';

// A thin Google Calendar v3 REST client. We only need a handful of calls, and
// plain fetch keeps the serverless bundle small.

const BASE = 'https://www.googleapis.com/calendar/v3';

export class GoogleApiError extends Error {
  constructor(public status: number, public body: string) {
    super(`Google Calendar API ${status}: ${body.slice(0, 300)}`);
  }
  get gone() {
    return this.status === 404 || this.status === 410;
  }
}

async function call<T>(token: string, path: string, init: RequestInit = {}, attempt = 0): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json', ...init.headers },
    cache: 'no-store',
  });
  if ((res.status === 429 || res.status >= 500 || (res.status === 403 && (await peekRateLimit(res)))) && attempt < 4) {
    await new Promise((r) => setTimeout(r, 2 ** attempt * 500 + Math.random() * 250));
    return call<T>(token, path, init, attempt + 1);
  }
  if (!res.ok) throw new GoogleApiError(res.status, await res.text());
  if (res.status === 204) return undefined as T;
  const text = await res.text();
  return (text ? JSON.parse(text) : undefined) as T;
}

async function peekRateLimit(res: Response): Promise<boolean> {
  const text = await res.clone().text();
  return /rateLimitExceeded|userRateLimitExceeded/.test(text);
}

const cal = (id: string) => encodeURIComponent(id);

export interface CalendarListEntry {
  id: string;
  summary: string;
  summaryOverride?: string;
  primary?: boolean;
  accessRole: 'freeBusyReader' | 'reader' | 'writer' | 'owner';
  backgroundColor?: string;
  timeZone?: string;
}

export async function listCalendars(token: string): Promise<CalendarListEntry[]> {
  const out: CalendarListEntry[] = [];
  let pageToken: string | undefined;
  do {
    const q = new URLSearchParams({ maxResults: '250', ...(pageToken ? { pageToken } : {}) });
    const page = await call<{ items?: CalendarListEntry[]; nextPageToken?: string }>(token, `/users/me/calendarList?${q}`);
    out.push(...(page.items ?? []));
    pageToken = page.nextPageToken;
  } while (pageToken);
  return out;
}

// Expanded instances (recurring series become individual events) in a window.
export async function listEvents(token: string, calendarId: string, timeMin: Date, timeMax: Date): Promise<GEvent[]> {
  const out: GEvent[] = [];
  let pageToken: string | undefined;
  do {
    const q = new URLSearchParams({
      singleEvents: 'true',
      showDeleted: 'false',
      maxResults: '2500',
      timeMin: timeMin.toISOString(),
      timeMax: timeMax.toISOString(),
      ...(pageToken ? { pageToken } : {}),
    });
    const page = await call<{ items?: GEvent[]; nextPageToken?: string }>(token, `/calendars/${cal(calendarId)}/events?${q}`);
    out.push(...(page.items ?? []));
    pageToken = page.nextPageToken;
  } while (pageToken);
  return out;
}

// sendUpdates=none: mirrors never email anyone.
export const insertEvent = (token: string, calendarId: string, body: GEventInput) =>
  call<GEvent>(token, `/calendars/${cal(calendarId)}/events?sendUpdates=none`, { method: 'POST', body: JSON.stringify(body) });

// Full replace (PUT), so fields a stricter rule drops are actually cleared.
export const updateEvent = (token: string, calendarId: string, eventId: string, body: GEventInput) =>
  call<GEvent>(token, `/calendars/${cal(calendarId)}/events/${encodeURIComponent(eventId)}?sendUpdates=none`, {
    method: 'PUT',
    body: JSON.stringify(body),
  });

export async function deleteEvent(token: string, calendarId: string, eventId: string): Promise<void> {
  try {
    await call<void>(token, `/calendars/${cal(calendarId)}/events/${encodeURIComponent(eventId)}?sendUpdates=none`, { method: 'DELETE' });
  } catch (err) {
    if (err instanceof GoogleApiError && err.gone) return;
    throw err;
  }
}

export interface WatchChannel {
  id: string;
  resourceId: string;
  expiration?: string;
}

export const watchEvents = (token: string, calendarId: string, channel: { id: string; address: string; token: string; ttlSeconds: number }) =>
  call<WatchChannel>(token, `/calendars/${cal(calendarId)}/events/watch`, {
    method: 'POST',
    body: JSON.stringify({ id: channel.id, type: 'web_hook', address: channel.address, token: channel.token, params: { ttl: String(channel.ttlSeconds) } }),
  });

export async function stopChannel(token: string, id: string, resourceId: string): Promise<void> {
  try {
    await call<void>(token, '/channels/stop', { method: 'POST', body: JSON.stringify({ id, resourceId }) });
  } catch (err) {
    if (err instanceof GoogleApiError && (err.gone || err.status === 400)) return;
    throw err;
  }
}
