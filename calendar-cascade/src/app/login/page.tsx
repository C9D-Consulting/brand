import { LoginForm } from './form';

export default async function LoginPage({ searchParams }: { searchParams: Promise<{ next?: string }> }) {
  const { next } = await searchParams;
  return (
    <div className="shell">
      <div className="login card">
        <span className="eyebrow">Calendar Cascade</span>
        <h1>Sign in</h1>
        <p className="muted small" style={{ margin: '8px 0 20px' }}>
          One operator, one password. Set it with <code>ADMIN_PASSWORD</code>.
        </p>
        <LoginForm next={next ?? '/'} />
      </div>
    </div>
  );
}
