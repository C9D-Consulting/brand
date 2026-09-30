import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getCalendar, getRule } from '@/lib/data';
import { RuleForm } from './form';

export default async function RulePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const rule = await getRule(id);
  if (!rule) notFound();
  const [source, target] = await Promise.all([getCalendar(rule.source_calendar_id), getCalendar(rule.target_calendar_id)]);
  if (!source || !target) notFound();
  return (
    <>
      <Link href="/" className="small">
        ← Cascade
      </Link>
      <span className="eyebrow" style={{ marginTop: 18 }}>
        Rule
      </span>
      <h1 className="row" style={{ gap: 12 }}>
        <span className="dot" style={{ background: source.color, width: 14, height: 14 }} />
        {source.label}
        <span className="muted">→</span>
        <span className="dot" style={{ background: target.color, width: 14, height: 14 }} />
        {target.label}
      </h1>
      <p className="lede">What an event on {source.label} becomes on {target.label}.</p>
      <RuleForm rule={rule} source={source} target={target} />
    </>
  );
}
