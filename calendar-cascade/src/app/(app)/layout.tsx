import Link from 'next/link';
import { logout } from '../actions';

export const maxDuration = 300;
export const dynamic = 'force-dynamic';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="shell">
      <header className="topbar">
        <Link href="/" className="brand">
          <b>Calendar Cascade</b>
          <span>C9D</span>
        </Link>
        <nav className="nav">
          <Link href="/">Cascade</Link>
          <Link href="/calendars">Calendars</Link>
          <Link href="/activity">Activity</Link>
        </nav>
        <form action={logout}>
          <button className="link small">Sign out</button>
        </form>
      </header>
      {children}
    </div>
  );
}
