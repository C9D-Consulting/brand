-- Calendar Cascade: schema.
-- The app talks to these tables with the service role key from server code only.
-- RLS is enabled with no policies, so the anon and authenticated roles see nothing.

create extension if not exists pgcrypto;

create table public.google_accounts (
  id uuid primary key default gen_random_uuid(),
  email text not null unique,
  refresh_token_enc text not null,
  access_token_enc text,
  access_token_expires_at timestamptz,
  scopes text,
  status text not null default 'active' check (status in ('active', 'error')),
  last_error text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.calendars (
  id uuid primary key default gen_random_uuid(),
  account_id uuid not null references public.google_accounts (id) on delete cascade,
  google_calendar_id text not null,
  label text not null,
  color text not null default '#d6743a',
  time_zone text,
  enabled boolean not null default true,
  -- Detail this calendar shares with others by default, used when rules are generated.
  outbound_detail text not null default 'full' check (outbound_detail in ('full', 'title', 'busy')),
  -- Privacy ceiling: nothing written to this calendar carries more detail than this.
  inbound_max_detail text not null default 'full' check (inbound_max_detail in ('full', 'title', 'busy')),
  sort_order integer not null default 0,
  watch_channel_id text unique,
  watch_resource_id text,
  watch_expires_at timestamptz,
  sync_locked_until timestamptz,
  sync_dirty boolean not null default false,
  last_synced_at timestamptz,
  last_sync_error text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (account_id, google_calendar_id)
);

create table public.rules (
  id uuid primary key default gen_random_uuid(),
  source_calendar_id uuid not null references public.calendars (id) on delete cascade,
  target_calendar_id uuid not null references public.calendars (id) on delete cascade,
  enabled boolean not null default true,
  detail text not null default 'full' check (detail in ('full', 'title', 'busy')),
  title_template text not null default '{{source}}: {{title}}',
  busy_title text not null default 'Block',
  include_description boolean not null default true,
  include_location boolean not null default true,
  include_attendees boolean not null default true,
  include_conference boolean not null default true,
  visibility text not null default 'default' check (visibility in ('default', 'public', 'private')),
  show_as text not null default 'busy' check (show_as in ('busy', 'free')),
  color_id text,
  keep_reminders boolean not null default false,
  buffer_before_min integer not null default 0 check (buffer_before_min between 0 and 240),
  buffer_after_min integer not null default 0 check (buffer_after_min between 0 and 240),
  buffer_title text not null default 'Buffer',
  skip_all_day boolean not null default true,
  skip_free boolean not null default true,
  skip_declined boolean not null default true,
  skip_tentative boolean not null default false,
  skip_if_native_on_target boolean not null default true,
  exclude_keywords text[] not null default array['#nocascade'],
  lookahead_days integer not null default 60 check (lookahead_days between 1 and 365),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (source_calendar_id, target_calendar_id),
  check (source_calendar_id <> target_calendar_id)
);

create table public.mirrors (
  id uuid primary key default gen_random_uuid(),
  rule_id uuid not null references public.rules (id) on delete cascade,
  source_calendar_id uuid not null references public.calendars (id) on delete cascade,
  source_event_id text not null,
  target_calendar_id uuid not null references public.calendars (id) on delete cascade,
  target_event_id text not null,
  kind text not null check (kind in ('main', 'buffer_before', 'buffer_after')),
  source_start timestamptz not null,
  source_end timestamptz not null,
  content_hash text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (rule_id, source_event_id, kind)
);

create index mirrors_source_window on public.mirrors (source_calendar_id, source_end);
create index mirrors_target_event on public.mirrors (target_calendar_id, target_event_id);

create table public.activity (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  level text not null default 'info' check (level in ('info', 'warn', 'error')),
  action text not null,
  calendar_id uuid references public.calendars (id) on delete set null,
  rule_id uuid references public.rules (id) on delete set null,
  message text not null,
  details jsonb
);

create index activity_recent on public.activity (created_at desc);

-- Take the per-calendar sync lock. Returns true when acquired; otherwise marks
-- the calendar dirty so the current holder runs one more pass before releasing.
create or replace function public.try_lock_calendar(p_calendar_id uuid, p_seconds integer)
returns boolean
language plpgsql
as $$
declare
  got boolean;
begin
  update public.calendars
     set sync_locked_until = now() + make_interval(secs => p_seconds),
         sync_dirty = false
   where id = p_calendar_id
     and (sync_locked_until is null or sync_locked_until < now())
  returning true into got;

  if got then
    return true;
  end if;

  update public.calendars set sync_dirty = true where id = p_calendar_id;
  return false;
end;
$$;

-- Release the lock. Returns true when another pass was requested while held.
create or replace function public.unlock_calendar(p_calendar_id uuid)
returns boolean
language plpgsql
as $$
declare
  was_dirty boolean;
begin
  select sync_dirty into was_dirty
    from public.calendars
   where id = p_calendar_id
     for update;

  update public.calendars
     set sync_locked_until = null,
         sync_dirty = false
   where id = p_calendar_id;
  return coalesce(was_dirty, false);
end;
$$;

alter table public.google_accounts enable row level security;
alter table public.calendars enable row level security;
alter table public.rules enable row level security;
alter table public.mirrors enable row level security;
alter table public.activity enable row level security;

revoke execute on function public.try_lock_calendar(uuid, integer) from public, anon, authenticated;
revoke execute on function public.unlock_calendar(uuid) from public, anon, authenticated;
