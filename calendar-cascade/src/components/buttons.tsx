'use client';

import { useFormStatus } from 'react-dom';

export function Submit({ children, pendingText, className }: { children: React.ReactNode; pendingText?: string; className?: string }) {
  const { pending } = useFormStatus();
  return (
    <button className={className} disabled={pending}>
      {pending ? (pendingText ?? 'Working…') : children}
    </button>
  );
}

export function ConfirmSubmit({ children, message, className }: { children: React.ReactNode; message: string; className?: string }) {
  const { pending } = useFormStatus();
  return (
    <button
      className={className}
      disabled={pending}
      onClick={(e) => {
        if (!confirm(message)) e.preventDefault();
      }}
    >
      {pending ? 'Working…' : children}
    </button>
  );
}

// A select that submits its form as soon as it changes.
export function AutoSelect(props: React.SelectHTMLAttributes<HTMLSelectElement>) {
  const { pending } = useFormStatus();
  return <select {...props} disabled={pending} onChange={(e) => e.currentTarget.form?.requestSubmit()} />;
}
