// Shared types. Row types mirror the Supabase tables column for column.

export type Detail = 'full' | 'title' | 'busy';
export type MirrorKind = 'main' | 'buffer_before' | 'buffer_after';

export const DETAILS: Detail[] = ['full', 'title', 'busy'];
export const DETAIL_RANK: Record<Detail, number> = { busy: 0, title: 1, full: 2 };
export const DETAIL_LABEL: Record<Detail, string> = {
  full: 'Full context',
  title: 'Title only',
  busy: 'Busy block',
};

export interface CalendarRow {
  id: string;
  account_id: string;
  google_calendar_id: string;
  label: string;
  color: string;
  time_zone: string | null;
  enabled: boolean;
  outbound_detail: Detail;
  inbound_max_detail: Detail;
  sort_order: number;
  watch_channel_id: string | null;
  watch_resource_id: string | null;
  watch_expires_at: string | null;
  last_synced_at: string | null;
  last_sync_error: string | null;
  created_at: string;
}

export interface RuleRow {
  id: string;
  source_calendar_id: string;
  target_calendar_id: string;
  enabled: boolean;
  detail: Detail;
  title_template: string;
  busy_title: string;
  include_description: boolean;
  include_location: boolean;
  include_attendees: boolean;
  include_conference: boolean;
  visibility: 'default' | 'public' | 'private';
  show_as: 'busy' | 'free';
  color_id: string | null;
  keep_reminders: boolean;
  buffer_before_min: number;
  buffer_after_min: number;
  buffer_title: string;
  skip_all_day: boolean;
  skip_free: boolean;
  skip_declined: boolean;
  skip_tentative: boolean;
  skip_if_native_on_target: boolean;
  exclude_keywords: string[];
  lookahead_days: number;
}

export interface MirrorRow {
  id: string;
  rule_id: string;
  source_calendar_id: string;
  source_event_id: string;
  target_calendar_id: string;
  target_event_id: string;
  kind: MirrorKind;
  source_start: string;
  source_end: string;
  content_hash: string;
}

// The subset of the Google Calendar event resource the engine reads or writes.
export interface GEventTime {
  date?: string;
  dateTime?: string;
  timeZone?: string;
}

export interface GAttendee {
  email?: string;
  displayName?: string;
  responseStatus?: 'needsAction' | 'declined' | 'tentative' | 'accepted';
  self?: boolean;
  organizer?: boolean;
  resource?: boolean;
  optional?: boolean;
}

export interface GEvent {
  id: string;
  status?: 'confirmed' | 'tentative' | 'cancelled';
  summary?: string;
  description?: string;
  location?: string;
  start?: GEventTime;
  end?: GEventTime;
  transparency?: 'opaque' | 'transparent';
  visibility?: 'default' | 'public' | 'private' | 'confidential';
  attendees?: GAttendee[];
  organizer?: { email?: string; displayName?: string; self?: boolean };
  hangoutLink?: string;
  conferenceData?: {
    entryPoints?: { entryPointType?: string; uri?: string; label?: string; pin?: string }[];
  };
  htmlLink?: string;
  iCalUID?: string;
  recurringEventId?: string;
  eventType?: string;
  extendedProperties?: {
    private?: Record<string, string>;
    shared?: Record<string, string>;
  };
}

// What we write to a target calendar. Sent with events.insert / events.update,
// so every field we omit is cleared on update.
export interface GEventInput {
  summary: string;
  description?: string;
  location?: string;
  start: GEventTime;
  end: GEventTime;
  transparency: 'opaque' | 'transparent';
  visibility: 'default' | 'public' | 'private';
  colorId?: string;
  reminders: { useDefault: boolean; overrides?: { method: string; minutes: number }[] };
  extendedProperties: { private: Record<string, string> };
}
