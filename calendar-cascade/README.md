# Calendar Cascade

Keeps several Google calendars blocked for one another. When an event lands on any calendar in the
cascade, a mirror of it is written to every other calendar: full context where you want it, a bare
busy block where you do not, with optional buffers either side.

Next.js on Vercel, Supabase Postgres as the datastore, Google Calendar push notifications as the trigger.

## What it does

The cascade is a matrix. Rows are where an event starts, columns are where its mirror lands, and each
cell is a **rule**:

| Level | What the target calendar gets |
| --- | --- |
| Full context | `Sayer: Quarterly planning`, with description, location, join links, organizer and attendees |
| Title only | `Sayer: Quarterly planning` and nothing else |
| Busy block | `Block`. No title, no details |
| Off | Nothing |

Every calendar also has a **policy**:

- **Shares with others**: the default level for rules leaving it.
- **Privacy ceiling**: the most detail it will ever accept. A rule asking for more is capped. Set the
  employer calendar to *Busy block* and no rule, template or mistake can leak detail onto it.

Adding a calendar creates rules to and from every other calendar from these two settings. The brief
this was built for is four calendars, all sharing *Full context*, with Sayer's ceiling at *Busy block*:

| From ↓ To → | Sayer | C9D Consulting | MonetizeKit | Brandon.Wilburn.Pro |
| --- | --- | --- | --- | --- |
| **Sayer** | | `Sayer: <title>` full | `Sayer: <title>` full | `Sayer: <title>` full |
| **C9D Consulting** | `Block` | | `C9D Consulting: <title>` full | `C9D Consulting: <title>` full |
| **MonetizeKit** | `Block` | `MonetizeKit: <title>` full | | `MonetizeKit: <title>` full |
| **Brandon.Wilburn.Pro** | `Block` | `Brandon.Wilburn.Pro: <title>` full | `Brandon.Wilburn.Pro: <title>` full | |

Each rule can then be customized on its own page, with a live preview:

- **Title template** with `{{source}}`, `{{title}}`, `{{organizer}}`, `{{location}}`; a separate busy title
  that can only use `{{source}}`.
- **What travels** in full mode: description, location, join links and dial-in, organizer and attendees.
  Attendees are listed in the description; mirrors never have guests, so nobody is ever invited or emailed.
- **Buffers** before and after timed events, written as separate busy events so the mirror keeps its real times.
- **Show as** busy or free, visibility, event colour, and whether the target's default reminders apply
  (off by default, so one meeting does not notify you four times).
- **Filters**: skip all-day events, events shown as free, declined events, tentative or unanswered
  invites, events already on the target through the same invitation, and events containing a keyword
  (`#nocascade` by default). A lookahead window in days.

Two rules always hold: an event marked **private** on its source only ever cascades as a busy block, and
events the cascade wrote itself are never cascaded again, so there are no loops.

## How it works

```
Google Calendar ──push──▶ /api/google/webhook ──▶ syncCalendar(source)
                                                   │  per-calendar lock in Postgres;
Vercel Cron ──daily──▶ /api/cron/sync ──▶ syncAll  │  bursts of pushes collapse into one pass
                                                   ▼
                                    reconcileSource(source)
                     1. list the source's events in the window (recurring series expanded)
                     2. load the mirrors already written
                     3. list each target (native invitations, hand-deleted mirrors, strays)
                     4. plan the desired mirrors (pure engine) and diff
                     5. create / update / delete on Google, record in `mirrors`
```

Reconciliation is idempotent. A pass with nothing to do writes nothing, so it is safe to run on every
push, on the cron, and from the **Sync** buttons. It also self-heals: a mirror deleted by hand is put
back, an edited or moved event is rewritten, a deleted or cancelled one is removed, and an event left
behind by an interrupted run is swept up. Changing a rule or a calendar's ceiling rewrites the existing
mirrors to match; turning a rule off or pausing a calendar removes them.

| Path | Holds |
| --- | --- |
| `src/lib/engine/` | The pure cascade engine: filters, privacy caps, templates, buffers, planning and diffing. No I/O, also runs in the browser for the rule preview |
| `src/lib/sync/` | Reconciler, lock-guarded runner, push channel management |
| `src/lib/google/` | OAuth (tokens AES-256-GCM encrypted at rest) and a small Calendar REST client |
| `src/app/` | Dashboard, server actions, OAuth, webhook and cron routes |
| `supabase/migrations/` | Schema: accounts, calendars, rules, mirrors, activity, lock functions |
| `test/` | Engine unit tests and reconciler integration tests against in-memory Google and Supabase |

## Setup

### 1. Supabase

Create a project and apply the migration, either with the Supabase CLI (`supabase db push`) or by
pasting `supabase/migrations/20260930000000_calendar_cascade.sql` into the SQL editor. RLS is on with no
policies: only the server, using the service role key, can read or write.

### 2. Google Cloud

1. Create a project and enable the **Google Calendar API**.
2. OAuth consent screen: add the scopes `calendar.events` and `calendar.calendarlist.readonly`. Add each
   Google account you will connect as a test user, or publish the app. In *Testing* status Google expires
   refresh tokens after seven days, so publish it (an unverified app is fine for your own accounts).
3. Credentials → OAuth client ID → *Web application*. Authorized redirect URI:
   `https://<your-domain>/api/google/callback` (and `http://localhost:3000/api/google/callback` for local).

A Google Workspace account (an employer's, say) may block third-party apps. If connecting it fails, ask
the admin to allow the app, or share that calendar with edit rights to an account you can connect and
add it from there.

### 3. Vercel

Import the repository with **Root Directory** set to `calendar-cascade`, and set the variables from
`.env.example`:

| Variable | Value |
| --- | --- |
| `APP_URL` | The production URL, `https://…`. Push notifications need https |
| `ADMIN_PASSWORD` | The dashboard password |
| `SESSION_SECRET` | `openssl rand -base64 32` |
| `TOKEN_ENCRYPTION_KEY` | `openssl rand -base64 32` (must decode to 32 bytes; changing it orphans stored tokens) |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | From step 2 |
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | From step 1 |
| `CRON_SECRET` | Any long random string; Vercel sends it to the cron route |

`vercel.json` schedules the safety-net cron daily, which Hobby plans allow and which is enough to renew
push channels (they last about a week). On Pro, tighten it to `*/15 * * * *` so a missed push is
caught within minutes.

### 4. Use it

1. Sign in, open **Calendars**, and connect each Google account.
2. Add the calendars you want in the cascade. Give each a label (it becomes the title prefix), and set
   the employer calendar's privacy ceiling to *Busy block*.
3. Open **Cascade**. The matrix is already filled in from the policies; adjust any cell, or open
   *Customize* for templates, buffers and filters.

## Local development

```bash
cp .env.example .env.local   # fill it in; APP_URL=http://localhost:3000
npm install
npm run dev
npm test          # engine + reconciler tests
npm run typecheck
```

Without an https `APP_URL`, Google cannot push changes, so use **Sync** in the dashboard.
