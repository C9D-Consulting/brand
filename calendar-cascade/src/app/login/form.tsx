'use client';

import { useActionState } from 'react';
import { login } from '../actions';

export function LoginForm({ next }: { next: string }) {
  const [state, action, pending] = useActionState(login, {});
  return (
    <form action={action} className="stack">
      <input type="hidden" name="next" value={next} />
      <label>
        Password
        <input type="password" name="password" autoFocus required autoComplete="current-password" />
      </label>
      {state?.error && <p className="notice err small">{state.error}</p>}
      <button disabled={pending}>{pending ? 'Checking…' : 'Sign in'}</button>
    </form>
  );
}
