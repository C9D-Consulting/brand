import { getActivity, getCalendars } from '@/lib/data';
import { ActivityList } from '@/components/activity';

export default async function ActivityPage() {
  const [rows, calendars] = await Promise.all([getActivity(200), getCalendars()]);
  return (
    <>
      <span className="eyebrow">Activity</span>
      <h1>Everything the cascade did.</h1>
      <p className="lede">Syncs that changed something, errors, and configuration changes. Quiet syncs are not logged.</p>
      <div className="section" style={{ marginTop: 28 }}>
        <ActivityList rows={rows} calendars={calendars} />
      </div>
    </>
  );
}
